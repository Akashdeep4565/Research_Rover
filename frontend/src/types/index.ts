// Basic types for the application
export interface Paper {
  source: string
  title: string
  download_url?: string
  year?: string
  keywords: string[]
  doi?: string
  pmid?: string
  openalex_id?: string
  authors?: string[]
  affiliations?: string | string[]
  countries?: string[]
  abstract?: string
  citation_count?: number | null
  is_oa?: boolean | null
  pdf_url?: string | null
  relevance_score?: number | null
  relevance_rank?: number | null
}

export type SortMode = 'relevance' | 'recency'

export interface SearchFilters {
  startDate?: string
  endDate?: string
  source: 'unified' | 'pubmed' | 'openalex'
  maxResults?: number
  sortMode?: SortMode
}

export interface CitationSource {
  id: number
  type: string
  content_preview: string
  title?: string
  url?: string
  doi?: string
  source?: string
  year?: number
}

export interface ChatMessage {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: number
  isError?: boolean
  sources?: CitationSource[]
  conversation_id?: string
  isStreaming?: boolean
}

// ─── Persistent Conversation Types (Phase 3) ─────────────────────────────────
export interface ConversationMessage {
  id: string
  conversation_id: string
  role: 'user' | 'assistant'
  content: string
  is_error: boolean
  sources?: CitationSource[]
  created_at: string
}

export interface Conversation {
  id: string
  title: string
  dataset_filename: string | null
  created_at: string
  updated_at: string
  messages: ConversationMessage[]
}

export interface ConversationSummary {
  id: string
  title: string
  dataset_filename: string | null
  message_count: number
  created_at: string
  updated_at: string
}

export type ConversationListItem = ConversationSummary

export interface ConversationCreate {
  title?: string
  dataset_filename?: string | null
}

export interface ConversationUpdate {
  title: string
}

export interface ConversationListResponse {
  conversations: ConversationSummary[]
  total: number
  limit: number
  offset: number
}

export type Theme = 'dark' | 'light' | 'system'

// ─── System Health & Status Types ───────────────────────────────────────────
export interface ModelComponentInfo {
  name: string
  status: 'loaded' | 'not_loaded' | 'loading' | 'error' | 'available' | 'unavailable' | 'not_configured' | 'disabled' | string
  type: 'local' | 'remote'
  required?: boolean
  details?: string | null
}

export interface ModelsStatusInfo {
  status: 'loaded' | 'partial' | 'loading' | 'not_loaded' | 'error' | string
  components: {
    embedding?: ModelComponentInfo
    reranker?: ModelComponentInfo
    llm?: ModelComponentInfo
    [key: string]: ModelComponentInfo | undefined
  }
}

export interface SystemStatusResponse {
  status: string
  api: 'online' | 'offline'
  version: string
  timestamp: number
  models: ModelsStatusInfo
  services?: Record<string, string>
}

// ─── Metadata-driven analytics (backend AnalysisService) ─────────────────────
export interface KeywordFrequencyItem {
  keyword: string
  frequency: number
  percentage: number
}

export interface CoOccurrenceEdge {
  source: string
  target: string
  weight: number
}

export interface CentralityScore {
  keyword: string
  degree_centrality: number
  closeness_centrality: number
  betweenness_centrality: number
  eigenvector_centrality: number
  clustering_coefficient: number
}

export interface AnalysisSourceInfo {
  filename: string
  paper_count: number
  has_keywords: boolean
}

export interface AnalysisSummary {
  filename: string
  source_file: string
  normalized_metadata_file: string
  keyword_frequency_file: string
  keyword_presence_matrix_file: string
  summary_file?: string
  generated_at: number
  minimum_frequency: number
  matrix_rows: number
  matrix_columns: number
  total_papers: number
  papers_with_keywords: number
  unique_keywords: number
  top_keywords_limit: number
  keyword_frequency: KeywordFrequencyItem[]
  cooccurrence_edges: CoOccurrenceEdge[]
  centrality_scores: CentralityScore[]
  matrix_keywords: string[]
}

export interface MatrixRow {
  paper_id: string
  title: string
  source: string
  year: string | null
  values: Record<string, number>
}

export interface KeywordMatrixResponse {
  matrix_keywords: string[]
  rows: MatrixRow[]
  total_rows: number
  total_columns: number
  truncated: boolean
}

export interface AnalysisRequest {
  filename: string
  top_keywords?: number
  minimum_frequency?: number
  refresh?: boolean
}

// ─── Country Collaboration Graph Types ────────────────────────────────────────
export interface CountryNode {
  id: string
  label: string
  iso_a3?: string
  paper_count: number
}

export interface CountryLink {
  source: string
  target: string
  weight: number
}

export interface CountryCollaborationGraphResponse {
  filename?: string
  nodes: CountryNode[]
  links: CountryLink[]
  total_papers: number
  papers_with_country_data: number
  papers_without_country_data?: number
  international_papers?: number
  country_coverage_percentage?: number
}

export interface CountryFrequencyItem {
  country: string
  iso_a3?: string
  frequency: number
  percentage: number
}

export interface UnassignedPaperInfo {
  paper_id: string
  title: string
  authors?: string | string[]
  source?: string
  year?: string
}

export interface CountryStatisticsResponse {
  filename?: string
  total_papers: number
  papers_with_country_data: number
  papers_without_country_data: number
  unique_countries: number
  international_papers: number
  country_coverage_percentage: number
  countries: CountryFrequencyItem[]
  unassigned_papers?: UnassignedPaperInfo[]
}

// ─── Canonical Dataset Ingestion & Quality Types (Phases 1-4) ──────────────────
export type FeatureReadinessStatus = 'ready' | 'partially_ready' | 'not_ready'

export interface ColumnMapping {
  original_column: string
  canonical_field?: string | null
  confidence: number
  matching_method: 'exact_canonical' | 'deterministic_alias' | 'normalized_alias' | 'fuzzy_match' | 'manual_override' | 'unmatched' | string
  status: 'matched' | 'conflict' | 'uncertain' | 'unmapped' | string
  details?: string | null
}

export interface NormalizationReport {
  total_columns: number
  mapped_columns: number
  unmapped_columns: number
  uncertain_columns: number
  conflicts: string[]
  mappings: Record<string, ColumnMapping>
  total_records: number
  valid_records: number
  duplicate_records: number
}

export interface FeatureReadiness {
  feature_name: string
  status: FeatureReadinessStatus
  required_fields: string[]
  available_fields: string[]
  missing_fields: string[]
  coverage_percentage: number
  warnings: string[]
  explanation: string
}

export interface FieldStatistics {
  field_name: string
  total_records: number
  populated_records: number
  missing_records: number
  invalid_records: number
  coverage_percentage: number
}

export interface DatasetQualityReport {
  overall_quality_score: number
  quality_grade: 'Excellent' | 'Good' | 'Fair' | 'Poor' | 'Critical' | string
  total_records: number
  valid_records: number
  duplicate_records: number
  field_statistics: Record<string, FieldStatistics>
  unmapped_columns: string[]
  feature_readiness: Record<string, FeatureReadiness>
  recommendations: string[]
  normalization_report?: NormalizationReport | null
}

export interface ExtendedFileUploadResponse {
  message: string
  filename: string
  encoding: string
  total_records: number
  valid_records: number
  duplicate_records: number
  overall_quality_score: number
  quality_grade: 'Excellent' | 'Good' | 'Fair' | 'Poor' | 'Critical' | string
  canonical_fields_detected: string[]
  column_mappings: Record<string, ColumnMapping>
  unmapped_columns: string[]
  conflicting_mappings: string[]
  feature_readiness: Record<string, FeatureReadiness>
  warnings: string[]
  recommendations: string[]
  index_status: 'indexed' | 'not_indexed' | string
}


