import axios, { type AxiosResponse } from 'axios'
import { createSSEParser, type ParsedSSEEvent } from './sseParser.ts'
import type {
  Paper,
  AnalysisRequest,
  AnalysisSummary,
  AnalysisSourceInfo,
  KeywordMatrixResponse,
  CountryCollaborationGraphResponse,
  CountryStatisticsResponse,
  SystemStatusResponse,
  ExtendedFileUploadResponse,
  DatasetQualityReport,
  Conversation,
  ConversationSummary,
  ConversationListItem,
  ConversationCreate,
  ConversationUpdate,
  ConversationListResponse,
  CitationSource,
} from '@/types'

// API Request/Response types
export interface SearchRequest {
  query: string
  page?: number
  per_page?: number
  max_results?: number
  start_date?: string
  end_date?: string
  search_source?: 'unified' | 'pubmed' | 'openalex'
  use_raw_query?: boolean
  sort_mode?: 'relevance' | 'recency'
}

export interface SearchResponse {
  results: Paper[]
  csv_filename: string
  total_results: number
  current_page: number
  total_pages: number
  per_page: number
  search_source: string
}

export interface SearchProgress {
  stage: number
  sub_stage: number
  message: string
  timestamp: number
  status: 'idle' | 'searching' | 'completed' | 'error' | 'cancelled'
  progress: number
  current_source?: string
  results_count?: number
}

export interface ChatHistoryMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatRequest {
  message: string
  filename?: string | null
  history?: ChatHistoryMessage[]
  conversation_id?: string | null
}

export interface ChatResponse {
  response: string
  sources?: CitationSource[]
  query?: string
  conversation_id?: string | null
  message_id?: string | null
}

export interface StreamStatusPayload {
  stage: 'retrieving' | 'generating' | string
  message: string
}

export interface StreamDonePayload {
  message_id: string | null
  conversation_id: string | null
  status: 'completed' | string
}

export interface StreamErrorPayload {
  error: string
  code?: string
}

export interface StreamChatOptions {
  onStatus?: (status: StreamStatusPayload) => void
  onCitations?: (sources: CitationSource[]) => void
  onDelta?: (text: string) => void
  onDone?: (done: StreamDonePayload) => void
  onError?: (error: StreamErrorPayload) => void
  signal?: AbortSignal
}

export interface FileInfo {
  filename: string
  size: number
  created_at: string
  type: string
}

export interface EmbeddingProgress {
  stage: number
  message: string
  timestamp: number
  percent?: number
}

export interface ApiError {
  error: string
  detail?: string
  code?: string
}

// Get base URL from environment variables
const getBaseURL = () => {
  return (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || 'http://localhost:8000/api/v1'
}

// Create axios instance
const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    let errorMessage = error.response?.data?.error || error.response?.data?.detail || error.message || 'An error occurred'
    let errorDetail = error.response?.data?.detail

    if (error.response?.data instanceof Blob) {
      try {
        const text = await error.response.data.text()
        const parsed = JSON.parse(text)
        errorMessage = parsed.error || parsed.detail || errorMessage
        errorDetail = parsed.detail
      } catch {
        // Blob wasn't JSON formatted
      }
    }

    const apiError: ApiError = {
      error: errorMessage,
      detail: errorDetail,
      code: error.response?.status?.toString(),
    }
    return Promise.reject(apiError)
  }
)

// Search API
export const searchApi = {
  search: async (request: SearchRequest): Promise<SearchResponse> => {
    const response: AxiosResponse<SearchResponse> = await api.post('/search/', request)
    return response.data
  },

  searchGet: async (params: SearchRequest): Promise<SearchResponse> => {
    const response: AxiosResponse<SearchResponse> = await api.get('/search/', { params })
    return response.data
  },

  getProgress: async (): Promise<SearchProgress> => {
    const response: AxiosResponse<SearchProgress> = await api.get('/search/progress')
    return response.data
  },

  cancel: async (): Promise<{ cancelled: boolean; message: string }> => {
    const response = await api.post('/search/cancel')
    return response.data
  },

  getResults: async (page: number = 1, perPage: number = 10): Promise<SearchResponse> => {
    const response: AxiosResponse<SearchResponse> = await api.get('/search/results', {
      params: { page, per_page: perPage },
    })
    return response.data
  },
}

// Files API
export const filesApi = {
  upload: async (file: File): Promise<ExtendedFileUploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    const response: AxiosResponse<ExtendedFileUploadResponse> = await api.post('/files/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  getQuality: async (filename: string): Promise<DatasetQualityReport> => {
    const response: AxiosResponse<DatasetQualityReport> = await api.get(
      `/files/${encodeURIComponent(filename)}/quality`
    )
    return response.data
  },

  download: async (filename: string): Promise<Blob> => {
    const response = await api.get(`/files/download/${filename}`, {
      responseType: 'blob',
    })
    return response.data
  },

  downloadPdf: async (
    url: string,
    title?: string,
    doi?: string,
    pmid?: string
  ): Promise<{ blob: Blob; filename: string }> => {
    const response = await api.get('/files/download-pdf', {
      params: { url, title, doi, pmid },
      responseType: 'blob',
    })

    let filename = ''
    const disposition = response.headers['content-disposition']
    if (disposition) {
      const match = disposition.match(/filename="?([^";]+)"?/i)
      if (match && match[1]) {
        filename = match[1]
      }
    }
    if (!filename) {
      const safeTitle = (title || 'research_paper').replace(/[^a-zA-Z0-9_\- ]/g, '').replace(/\s+/g, '_').slice(0, 80)
      filename = `${safeTitle || 'research_paper'}.pdf`
    }
    return { blob: response.data, filename }
  },

  getCsvData: async (filename: string): Promise<Paper[]> => {
    const response: AxiosResponse<Paper[]> = await api.get(`/files/csv/${filename}/data`)
    return response.data
  },

  getPaginatedCsvData: async (
    filename: string,
    page: number = 1,
    perPage: number = 10
  ): Promise<{
    results: Paper[]
    total_results: number
    current_page: number
    total_pages: number
    per_page: number
  }> => {
    const response = await api.get(`/files/csv/${filename}/paginated`, {
      params: { page, per_page: perPage },
    })
    return response.data
  },

  list: async (): Promise<FileInfo[]> => {
    const response: AxiosResponse<FileInfo[]> = await api.get('/files/list')
    return response.data
  },

  delete: async (filename: string): Promise<{ message: string }> => {
    const response = await api.delete(`/files/${filename}`)
    return response.data
  },
}

// Re-export conversation types for convenience
export type {
  Conversation,
  ConversationSummary,
  ConversationListItem,
  ConversationCreate,
  ConversationUpdate,
  ConversationListResponse,
  CitationSource,
}

// Conversations API (Phase 3 Backend Persistence)
export const conversationsApi = {
  list: async (
    dataset_filename?: string | null,
    limit: number = 50,
    offset: number = 0
  ): Promise<ConversationListResponse> => {
    const params: Record<string, any> = { limit, offset }
    if (dataset_filename !== undefined && dataset_filename !== null) {
      params.dataset_filename = dataset_filename
    }
    const response: AxiosResponse<ConversationListResponse> = await api.get('/chat/conversations', { params })
    return response.data
  },

  get: async (conversationId: string): Promise<Conversation> => {
    const response: AxiosResponse<Conversation> = await api.get(`/chat/conversations/${conversationId}`)
    return response.data
  },

  create: async (data: ConversationCreate): Promise<Conversation> => {
    const response: AxiosResponse<Conversation> = await api.post('/chat/conversations', data)
    return response.data
  },

  rename: async (conversationId: string, title: string): Promise<ConversationSummary> => {
    const payload: ConversationUpdate = { title }
    const response: AxiosResponse<ConversationSummary> = await api.patch(
      `/chat/conversations/${conversationId}`,
      payload
    )
    return response.data
  },

  delete: async (conversationId: string): Promise<{ message: string; data?: { conversation_id: string } }> => {
    const response = await api.delete(`/chat/conversations/${conversationId}`)
    return response.data
  },
}

// Chat API
export const chatApi = {
  sendMessage: async (
    filename: string,
    request: ChatRequest,
    signal?: AbortSignal
  ): Promise<ChatResponse> => {
    const response: AxiosResponse<ChatResponse> = await api.post(`/chat/${filename}`, request, {
      signal,
    })
    return response.data
  },

  sendMessageBody: async (
    request: ChatRequest,
    signal?: AbortSignal
  ): Promise<ChatResponse> => {
    const response: AxiosResponse<ChatResponse> = await api.post('/chat/', request, {
      signal,
    })
    return response.data
  },

  streamMessage: async (
    request: ChatRequest,
    options: StreamChatOptions
  ): Promise<void> => {
    const url = `${getBaseURL()}/chat/stream`

    let response: Response
    try {
      response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify(request),
        signal: options.signal,
      })
    } catch (err: any) {
      if (options.signal?.aborted || err?.name === 'AbortError') {
        throw err
      }
      throw new Error(err?.message || 'Failed to establish connection to streaming endpoint')
    }

    if (!response.ok) {
      let errorDetail = `HTTP ${response.status}`
      try {
        const errorJson = await response.json()
        errorDetail = errorJson.detail || errorJson.error || errorDetail
      } catch {
        const errorText = await response.text()
        if (errorText) errorDetail = errorText
      }

      const statusError = new Error(errorDetail) as any
      statusError.status = response.status
      statusError.code = String(response.status)
      throw statusError
    }

    if (!response.body) {
      throw new Error('Streaming response body is missing')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')

    const parser = createSSEParser({
      onEvent: (event: ParsedSSEEvent) => {
        switch (event.event) {
          case 'status':
            options.onStatus?.(event.data)
            break
          case 'citations':
            options.onCitations?.(event.data?.sources || [])
            break
          case 'delta':
            if (event.data?.text !== undefined) {
              options.onDelta?.(event.data.text)
            }
            break
          case 'done':
            options.onDone?.(event.data)
            break
          case 'error':
            options.onError?.(event.data)
            break
          default:
            break
        }
      },
      onError: (err) => {
        console.warn('SSE parse error:', err)
      },
    })

    try {
      while (true) {
        if (options.signal?.aborted) {
          await reader.cancel()
          break
        }

        const { done, value } = await reader.read()
        if (done) {
          parser.flush()
          break
        }

        if (value) {
          const textChunk = decoder.decode(value, { stream: true })
          parser.feed(textChunk)
        }
      }
    } finally {
      reader.releaseLock()
    }
  },
}

// Embeddings API
export interface EmbeddingOptions {
  scrape_full_text?: boolean
  max_scrape?: number
  force?: boolean
}

export const embeddingsApi = {
  create: async (
    filename: string,
    options?: EmbeddingOptions
  ): Promise<{ message: string }> => {
    const response = await api.post(`/embeddings/${filename}`, options ?? {})
    return response.data
  },

  getProgress: async (): Promise<EmbeddingProgress> => {
    const response: AxiosResponse<EmbeddingProgress> = await api.get('/embeddings/progress')
    return response.data
  },

  cancel: async (): Promise<{ cancelled: boolean; message: string }> => {
    const response = await api.post('/embeddings/cancel')
    return response.data
  },

  delete: async (filename: string): Promise<{ message: string }> => {
    const response = await api.delete(`/embeddings/${filename}`)
    return response.data
  },

  getStatus: async (filename: string): Promise<{
    filename: string
    embeddings_exist: boolean
    files: Array<{
      filename: string
      size: number
      created_at: number
    }>
    total_files: number
  }> => {
    const response = await api.get(`/embeddings/${filename}/status`)
    return response.data
  },
}

// Metadata-driven analytics — backed by the server's AnalysisService
// (keyword frequency, co-occurrence graph, and networkx centralities).
export const analysisApi = {
  listFiles: async (): Promise<AnalysisSourceInfo[]> => {
    const response: AxiosResponse<AnalysisSourceInfo[]> = await api.get('/analysis/files')
    return response.data
  },
  generate: async (request: AnalysisRequest): Promise<AnalysisSummary> => {
    const response: AxiosResponse<AnalysisSummary> = await api.post('/analysis/generate', request)
    return response.data
  },
  getSummary: async (filename: string, refresh = false): Promise<AnalysisSummary> => {
    const response: AxiosResponse<AnalysisSummary> = await api.get(
      `/analysis/${encodeURIComponent(filename)}/summary`, { params: { refresh } },
    )
    return response.data
  },
  getMatrix: async (filename: string, previewRows = 25): Promise<KeywordMatrixResponse> => {
    const response: AxiosResponse<KeywordMatrixResponse> = await api.get(
      `/analysis/${encodeURIComponent(filename)}/matrix`,
      { params: { preview_rows: Math.min(Math.max(previewRows, 1), 100) } },
    )
    return response.data
  },
  getCountryCollaboration: async (filename: string): Promise<CountryCollaborationGraphResponse> => {
    const response: AxiosResponse<CountryCollaborationGraphResponse> = await api.get(
      `/analysis/${encodeURIComponent(filename)}/country-collaboration`
    )
    return response.data
  },
  getCountryStatistics: async (filename: string): Promise<CountryStatisticsResponse> => {
    const response: AxiosResponse<CountryStatisticsResponse> = await api.get(
      `/analysis/${encodeURIComponent(filename)}/countries`
    )
    return response.data
  },
}

// System and Health check API
export const systemApi = {
  getStatus: async (signal?: AbortSignal): Promise<SystemStatusResponse> => {
    const response: AxiosResponse<SystemStatusResponse> = await api.get('/system/status', {
      timeout: 5000,
      signal,
    })
    return response.data
  },
}

export const healthApi = {
  check: async (signal?: AbortSignal): Promise<SystemStatusResponse> => {
    return systemApi.getStatus(signal)
  },
}

export default api
