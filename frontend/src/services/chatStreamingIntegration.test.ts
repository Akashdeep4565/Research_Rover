import test from 'node:test'
import assert from 'node:assert/strict'
import {
  chatApi,
  type StreamErrorPayload,
  type StreamDonePayload,
} from './api.ts'

function createMockStream(chunks: string[], status = 200, statusText = 'OK') {
  const encoder = new TextEncoder()
  let index = 0

  const stream = new ReadableStream({
    pull(controller) {
      if (index < chunks.length) {
        controller.enqueue(encoder.encode(chunks[index]))
        index++
      } else {
        controller.close()
      }
    },
  })

  return new Response(stream, {
    status,
    statusText,
    headers: { 'Content-Type': 'text/event-stream' },
  })
}

test('Streaming Integration: Citations arrive before first text delta', async () => {
  const originalFetch = globalThis.fetch

  const chunks = [
    'event: status\ndata: {"stage":"retrieving","message":"Reading..."}\n\n',
    'event: citations\ndata: {"sources":[{"id":1,"type":"paper","title":"Paper A","content_preview":"Abstract"}]}\n\n',
    'event: delta\ndata: {"text":"First token"}\n\n',
    'event: done\ndata: {"message_id":"msg-1","conversation_id":"c-1","status":"completed"}\n\n',
  ]

  globalThis.fetch = async () => createMockStream(chunks) as any

  try {
    let citationsReceivedFirst = false
    let deltaReceived = false
    let sourcesCount = 0

    await chatApi.streamMessage({ message: 'query' }, {
      onCitations: (sources) => {
        citationsReceivedFirst = !deltaReceived
        sourcesCount = sources.length
      },
      onDelta: () => {
        deltaReceived = true
      },
    })

    assert.equal(citationsReceivedFirst, true, 'Citations must arrive before any delta')
    assert.equal(sourcesCount, 1)
    assert.equal(deltaReceived, true)
  } finally {
    globalThis.fetch = originalFetch
  }
})

test('Streaming Integration: Server error before first delta is delivered cleanly', async () => {
  const originalFetch = globalThis.fetch

  const chunks = [
    'event: status\ndata: {"stage":"generating","message":"Connecting to AI..."}\n\n',
    'event: error\ndata: {"error":"503 Service Unavailable","code":"SERVICE_UNAVAILABLE"}\n\n',
  ]

  globalThis.fetch = async () => createMockStream(chunks) as any

  try {
    let capturedError: StreamErrorPayload | null = null
    const deltas: string[] = []

    await chatApi.streamMessage({ message: 'test' }, {
      onDelta: (d) => deltas.push(d),
      onError: (err) => {
        capturedError = err
      },
    })

    assert.equal(deltas.length, 0, 'No deltas should be emitted on early failure')
    assert.ok(capturedError !== null)
    assert.equal((capturedError as StreamErrorPayload).code, 'SERVICE_UNAVAILABLE')
  } finally {
    globalThis.fetch = originalFetch
  }
})

test('Streaming Integration: Server error after partial output preserves deltas', async () => {
  const originalFetch = globalThis.fetch

  const chunks = [
    'event: delta\ndata: {"text":"Partial text before drop. "}\n\n',
    'event: error\ndata: {"error":"Mid-stream connection drop","code":"GENERATION_ERROR"}\n\n',
  ]

  globalThis.fetch = async () => createMockStream(chunks) as any

  try {
    const deltas: string[] = []
    let capturedError: StreamErrorPayload | null = null

    await chatApi.streamMessage({ message: 'test' }, {
      onDelta: (d) => deltas.push(d),
      onError: (err) => {
        capturedError = err
      },
    })

    assert.equal(deltas.length, 1)
    assert.equal(deltas[0], 'Partial text before drop. ')
    assert.ok(capturedError !== null)
    assert.equal((capturedError as StreamErrorPayload).error, 'Mid-stream connection drop')
  } finally {
    globalThis.fetch = originalFetch
  }
})

test('Streaming Integration: Aborting stream cancels reader and halts callbacks', async () => {
  const originalFetch = globalThis.fetch
  const controller = new AbortController()

  let chunkCount = 0
  const endlessStream = new ReadableStream({
    pull(c) {
      chunkCount++
      c.enqueue(new TextEncoder().encode(`event: delta\ndata: {"text":"chunk${chunkCount}"}\n\n`))
    },
  })

  globalThis.fetch = async () =>
    new Response(endlessStream, {
      status: 200,
      headers: { 'Content-Type': 'text/event-stream' },
    }) as any

  try {
    const received: string[] = []
    await chatApi.streamMessage({ message: 'test' }, {
      signal: controller.signal,
      onDelta: (text) => {
        received.push(text)
        if (received.length >= 2) {
          controller.abort()
        }
      },
    })

    assert.equal(received.length, 2)
  } finally {
    globalThis.fetch = originalFetch
  }
})

test('Streaming Integration: Conversation switching ignores late arrivals', async () => {
  let activeConvoId = 'conversation-A'
  const messagesForConvoA: string[] = []
  const messagesForConvoB: string[] = []

  const originalFetch = globalThis.fetch
  const chunks = [
    'event: delta\ndata: {"text":"Token for A"}\n\n',
    'event: delta\ndata: {"text":"Late token"}\n\n',
  ]

  globalThis.fetch = async () => createMockStream(chunks) as any

  try {
    const reqConvoId = 'conversation-A'
    await chatApi.streamMessage({ message: 'test', conversation_id: reqConvoId }, {
      onDelta: (text) => {
        // Stale response guard implementation
        if (reqConvoId !== activeConvoId) {
          // Ignored
          return
        }
        messagesForConvoA.push(text)
        // User switches conversation to B
        activeConvoId = 'conversation-B'
      },
    })

    assert.equal(messagesForConvoA.length, 1)
    assert.equal(messagesForConvoA[0], 'Token for A')
    assert.equal(messagesForConvoB.length, 0)
  } finally {
    globalThis.fetch = originalFetch
  }
})

test('Streaming Integration: Done event reconciles message_id and conversation_id', async () => {
  const originalFetch = globalThis.fetch

  const chunks = [
    'event: delta\ndata: {"text":"Final answer."}\n\n',
    'event: done\ndata: {"message_id":"asst-persisted-uuid-999","conversation_id":"convo-persistent-111","status":"completed"}\n\n',
  ]

  globalThis.fetch = async () => createMockStream(chunks) as any

  try {
    let doneResult: StreamDonePayload | null = null

    await chatApi.streamMessage({ message: 'test' }, {
      onDone: (payload) => {
        doneResult = payload
      },
    })

    assert.ok(doneResult !== null)
    assert.equal((doneResult as StreamDonePayload).message_id, 'asst-persisted-uuid-999')
    assert.equal((doneResult as StreamDonePayload).conversation_id, 'convo-persistent-111')
    assert.equal((doneResult as StreamDonePayload).status, 'completed')
  } finally {
    globalThis.fetch = originalFetch
  }
})
