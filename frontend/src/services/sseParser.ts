/**
 * Standalone, robust Server-Sent Events (SSE) stream parser.
 * Conforms to the W3C SSE standard:
 * - Buffers incomplete events across network chunks.
 * - Handles multiple events in a single network chunk.
 * - Supports events split across arbitrary chunk boundaries.
 * - Supports multiline data fields and comments.
 * - Flushes any trailing buffered event upon stream closure.
 */

export interface ParsedSSEEvent {
  event: string
  data: any
}

export interface SSEParserOptions {
  onEvent: (event: ParsedSSEEvent) => void
  onError?: (error: Error) => void
}

export interface SSEParser {
  feed: (chunk: string) => void
  flush: () => void
  reset: () => void
}

export function createSSEParser(options: SSEParserOptions): SSEParser {
  let buffer = ''

  const parseEventBlock = (block: string) => {
    const lines = block.split(/\r?\n/)
    let eventName = ''
    const dataLines: string[] = []

    for (const rawLine of lines) {
      const line = rawLine.trimStart()

      // Ignore comments and empty lines inside block
      if (!line || line.startsWith(':')) {
        continue
      }

      if (line.startsWith('event:')) {
        eventName = line.slice(6).trim()
      } else if (line.startsWith('data:')) {
        dataLines.push(line.slice(5).trim())
      }
    }

    if (dataLines.length > 0 || eventName) {
      const rawData = dataLines.join('\n')
      let parsedData: any = rawData

      if (rawData) {
        try {
          parsedData = JSON.parse(rawData)
        } catch {
          // If not JSON, retain as raw string
          parsedData = rawData
        }
      }

      try {
        options.onEvent({
          event: eventName || 'message',
          data: parsedData,
        })
      } catch (err: any) {
        options.onError?.(err)
      }
    }
  }

  const feed = (chunk: string) => {
    buffer += chunk

    // Normalize Windows CRLF to LF for consistent block boundary detection
    const normalized = buffer.replace(/\r\n/g, '\n')
    const blocks = normalized.split('\n\n')

    // The last element is either empty (if ended on \n\n) or the incomplete remainder
    buffer = blocks.pop() || ''

    for (const block of blocks) {
      if (block.trim()) {
        parseEventBlock(block)
      }
    }
  }

  const flush = () => {
    if (buffer.trim()) {
      parseEventBlock(buffer)
      buffer = ''
    }
  }

  const reset = () => {
    buffer = ''
  }

  return { feed, flush, reset }
}
