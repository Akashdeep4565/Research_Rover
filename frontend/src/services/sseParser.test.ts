import test from 'node:test'
import assert from 'node:assert/strict'
import { createSSEParser, type ParsedSSEEvent } from './sseParser.ts'

test('SSE Parser: single complete event', () => {
  const events: ParsedSSEEvent[] = []
  const parser = createSSEParser({ onEvent: (e) => events.push(e) })

  parser.feed('event: delta\ndata: {"text":"Hello"}\n\n')

  assert.equal(events.length, 1)
  assert.equal(events[0].event, 'delta')
  assert.deepEqual(events[0].data, { text: 'Hello' })
})

test('SSE Parser: multiple events in a single chunk', () => {
  const events: ParsedSSEEvent[] = []
  const parser = createSSEParser({ onEvent: (e) => events.push(e) })

  const chunk = [
    'event: status\ndata: {"stage":"generating"}\n\n',
    'event: delta\ndata: {"text":"First"}\n\n',
    'event: delta\ndata: {"text":"Second"}\n\n',
  ].join('')

  parser.feed(chunk)

  assert.equal(events.length, 3)
  assert.equal(events[0].event, 'status')
  assert.equal(events[1].event, 'delta')
  assert.equal(events[1].data.text, 'First')
  assert.equal(events[2].event, 'delta')
  assert.equal(events[2].data.text, 'Second')
})

test('SSE Parser: fragmented event split across multiple chunks', () => {
  const events: ParsedSSEEvent[] = []
  const parser = createSSEParser({ onEvent: (e) => events.push(e) })

  parser.feed('event: ci')
  assert.equal(events.length, 0)

  parser.feed('tations\ndata: {"sour')
  assert.equal(events.length, 0)

  parser.feed('ces":[{"id":1,"title":"Paper A"}]}\n\n')
  assert.equal(events.length, 1)
  assert.equal(events[0].event, 'citations')
  assert.deepEqual(events[0].data, { sources: [{ id: 1, title: 'Paper A' }] })
})

test('SSE Parser: CRLF line endings', () => {
  const events: ParsedSSEEvent[] = []
  const parser = createSSEParser({ onEvent: (e) => events.push(e) })

  parser.feed('event: delta\r\ndata: {"text":"CRLF Token"}\r\n\r\n')

  assert.equal(events.length, 1)
  assert.equal(events[0].event, 'delta')
  assert.equal(events[0].data.text, 'CRLF Token')
})

test('SSE Parser: comments and empty lines are safely ignored', () => {
  const events: ParsedSSEEvent[] = []
  const parser = createSSEParser({ onEvent: (e) => events.push(e) })

  parser.feed(': keep-alive ping\n\nevent: delta\ndata: {"text":"Valid"}\n\n')

  assert.equal(events.length, 1)
  assert.equal(events[0].event, 'delta')
  assert.equal(events[0].data.text, 'Valid')
})

test('SSE Parser: trailing un-terminated event processed on flush()', () => {
  const events: ParsedSSEEvent[] = []
  const parser = createSSEParser({ onEvent: (e) => events.push(e) })

  parser.feed('event: done\ndata: {"status":"completed"}')
  assert.equal(events.length, 0)

  parser.flush()
  assert.equal(events.length, 1)
  assert.equal(events[0].event, 'done')
  assert.equal(events[0].data.status, 'completed')
})

test('SSE Parser: raw non-JSON text data preserved', () => {
  const events: ParsedSSEEvent[] = []
  const parser = createSSEParser({ onEvent: (e) => events.push(e) })

  parser.feed('event: raw\ndata: Plain string message\n\n')

  assert.equal(events.length, 1)
  assert.equal(events[0].event, 'raw')
  assert.equal(events[0].data, 'Plain string message')
})

test('SSE Parser: UTF-8 characters across chunk boundaries', () => {
  const events: ParsedSSEEvent[] = []
  const parser = createSSEParser({ onEvent: (e) => events.push(e) })

  // Construct raw UTF-8 bytes for 'event: delta\ndata: {"text":"🔬 Analysis"}\n\n'
  const text = 'event: delta\ndata: {"text":"🔬 Analysis"}\n\n'
  const encoder = new TextEncoder()
  const bytes = encoder.encode(text)

  // Split in the middle of the emoji (e.g. at byte 30)
  const decoder = new TextDecoder('utf-8')
  const chunk1 = decoder.decode(bytes.slice(0, 30), { stream: true })
  const chunk2 = decoder.decode(bytes.slice(30), { stream: false })

  parser.feed(chunk1)
  parser.feed(chunk2)

  assert.equal(events.length, 1)
  assert.equal(events[0].event, 'delta')
  assert.equal(events[0].data.text, '🔬 Analysis')
})
