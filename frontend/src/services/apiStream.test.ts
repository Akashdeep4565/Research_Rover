import test from 'node:test'
import assert from 'node:assert/strict'
import { chatApi, type ChatRequest, type StreamStatusPayload, type StreamDonePayload } from './api.ts'
import type { CitationSource } from '../types/index.ts'

// Mock global fetch for streaming tests
function createMockStreamResponse(chunks: string[], status = 200, statusText = 'OK') {
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

test('chatApi.streamMessage: parses stream events end-to-end', async () => {
  const originalFetch = globalThis.fetch

  const mockChunks = [
    'event: status\ndata: {"stage":"retrieving","message":"Searching papers..."}\n\n',
    'event: citations\ndata: {"sources":[{"id":1,"type":"research_paper","title":"Attention Is All You Need","url":"","doi":"10.1234/567","source":"arXiv","year":2017,"content_preview":"Transformer architecture"}]}\n\n',
    'event: delta\ndata: {"text":"Attention "}\n\n',
    'event: delta\ndata: {"text":"mechanisms."}\n\n',
    'event: done\ndata: {"message_id":"msg-123","conversation_id":"convo-456","status":"completed"}\n\n',
  ]

  globalThis.fetch = async () => createMockStreamResponse(mockChunks) as any

  try {
    const statuses: StreamStatusPayload[] = []
    let receivedCitations: CitationSource[] = []
    const deltas: string[] = []
    let completedDone: StreamDonePayload | null = null

    const req: ChatRequest = {
      message: 'Explain attention',
      conversation_id: 'convo-456',
    }

    await chatApi.streamMessage(req, {
      onStatus: (s) => statuses.push(s),
      onCitations: (c) => {
        receivedCitations = c
      },
      onDelta: (d) => deltas.push(d),
      onDone: (d) => {
        completedDone = d
      },
    })

    assert.equal(statuses.length, 1)
    assert.equal(statuses[0].stage, 'retrieving')
    assert.equal(receivedCitations.length, 1)
    assert.equal(receivedCitations[0].title, 'Attention Is All You Need')
    assert.deepEqual(deltas, ['Attention ', 'mechanisms.'])
    assert.ok(completedDone !== null)
    assert.equal((completedDone as StreamDonePayload).message_id, 'msg-123')
    assert.equal((completedDone as StreamDonePayload).status, 'completed')
  } finally {
    globalThis.fetch = originalFetch
  }
})

test('chatApi.streamMessage: throws on non-200 HTTP responses before reading stream', async () => {
  const originalFetch = globalThis.fetch

  globalThis.fetch = async () =>
    new Response(JSON.stringify({ detail: 'Dataset mismatch: bound to dataset_a.csv' }), {
      status: 400,
      statusText: 'Bad Request',
      headers: { 'Content-Type': 'application/json' },
    }) as any

  try {
    const req: ChatRequest = {
      message: 'Hello',
      conversation_id: 'convo-1',
      filename: 'dataset_b.csv',
    }

    await assert.rejects(
      async () => {
        await chatApi.streamMessage(req, {})
      },
      (err: any) => {
        assert.match(err.message, /Dataset mismatch/)
        assert.equal(err.status, 400)
        return true
      }
    )
  } finally {
    globalThis.fetch = originalFetch
  }
})

test('chatApi.streamMessage: handles user cancellation via AbortSignal', async () => {
  const originalFetch = globalThis.fetch
  const controller = new AbortController()

  // Response with endless chunks unless aborted
  const stream = new ReadableStream({
    pull(c) {
      c.enqueue(new TextEncoder().encode('event: delta\ndata: {"text":"token"}\n\n'))
    },
  })

  globalThis.fetch = async () =>
    new Response(stream, {
      status: 200,
      headers: { 'Content-Type': 'text/event-stream' },
    }) as any

  try {
    const deltas: string[] = []
    const req: ChatRequest = { message: 'Stream endless' }

    const streamPromise = chatApi.streamMessage(req, {
      signal: controller.signal,
      onDelta: (t) => {
        deltas.push(t)
        // Abort after first token
        controller.abort()
      },
    })

    // Should complete cleanly or terminate without throwing unhandled rejection
    await streamPromise
    assert.ok(deltas.length >= 1)
  } finally {
    globalThis.fetch = originalFetch
  }
})
