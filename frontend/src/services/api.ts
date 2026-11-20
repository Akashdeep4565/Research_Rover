import axios, { AxiosResponse } from 'axios'
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

export interface ChatRequest {
  message: string
  filename?: string
}

export interface ChatResponse {
  response: string
  sources?: Array<{
    id: number
    type: string
    content_preview: string
  }>
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
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
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
