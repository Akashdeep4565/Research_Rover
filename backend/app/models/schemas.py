"""
Pydantic models for request/response schemas
"""

from datetime import date
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum
import re

class SearchSource(str, Enum):
    """Available search sources"""
    CORE = "core"
    PUBMED = "pubmed"
    OPENALEX = "openalex"
    UNIFIED = "unified"

class SearchRequest(BaseModel):
    """Search request model"""
    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(10, ge=1, description="Results per page")
    max_results: int = Field(10, ge=1, description="Maximum results to fetch")
    start_date: Optional[date] = Field(None, description="Start date filter")
    end_date: Optional[date] = Field(None, description="End date filter")
    search_source: SearchSource = Field(SearchSource.UNIFIED, description="Search source: unified (default), pubmed, openalex")
    use_raw_query: bool = Field(True, description="Pass query directly to PubMed without synonym/MeSH expansion")
    sort_mode: str = Field(
        "relevance",
        description="Result ordering: 'relevance' = MedCPT semantic re-rank, 'recency' = newest first (PubMed order)",
    )

    @validator('end_date')
    def validate_date_range(cls, v, values):
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError('end_date must be greater than or equal to start_date')
        return v

class Paper(BaseModel):
    """Paper model"""
    source: str = Field(..., description="Paper source (e.g. pubmed, openalex, pubmed, openalex)")
    title: str = Field(..., description="Paper title")
    download_url: Optional[str] = Field(None, description="Download URL")
    year: Optional[str] = Field(None, description="Publication year")
    keywords: List[str] = Field(default_factory=list, description="Paper keywords")
    doi: Optional[str] = Field(None, description="DOI")
    pmid: Optional[str] = Field(None, description="PMID")
    openalex_id: Optional[str] = Field(None, description="OpenAlex ID")
    authors: Optional[List[str]] = Field(default_factory=list, description="Authors")
    affiliations: Optional[Union[str, List[str]]] = Field(None, description="Affiliations")
    countries: Optional[List[str]] = Field(default_factory=list, description="Countries")
    abstract: Optional[str] = Field(None, description="Abstract")
    citation_count: Optional[int] = Field(None, description="Citation count")
    is_oa: Optional[bool] = Field(None, description="Open Access status")
    pdf_url: Optional[str] = Field(None, description="PDF URL")
    relevance_score: Optional[float] = Field(
        None, description="MedCPT semantic relevance to the query (0-100, relative within this result set)"
    )
    relevance_rank: Optional[int] = Field(
        None, description="1-based rank assigned by the semantic re-ranker"
    )

class SearchResponse(BaseModel):
    """Search response model"""
    results: List[Paper]
    csv_filename: str
    total_results: int
    current_page: int
    total_pages: int
    per_page: int
    search_source: str

class SearchProgress(BaseModel):
    """Search progress model"""
    stage: int = Field(..., description="Current stage (0-4, -1 for error)")
    sub_stage: int = Field(0, description="Sub-stage within current stage")
    message: str = Field(..., description="Progress message")
    timestamp: float = Field(..., description="Timestamp")
    status: str = Field("idle", description="Status: idle, searching, completed, error, cancelled")
    progress: int = Field(0, description="Progress percentage (0-100)")

class EmbeddingProgress(BaseModel):
    """Embedding progress model"""
    stage: int = Field(..., description="Current stage (0-3, -1 for error)")
    message: str = Field(..., description="Progress message")
    timestamp: float = Field(..., description="Timestamp")
    percent: Optional[float] = Field(None, description="Overall completion percent (0-100)")

class EmbeddingOptions(BaseModel):
    """Optional per-request overrides for embedding creation."""
    scrape_full_text: Optional[bool] = Field(None, description="Scrape paper URLs for full text (slower, richer). Falls back to abstracts when False.")
    max_scrape: Optional[int] = Field(None, ge=0, description="Cap the number of URLs to scrape (0 = no cap).")
    force: Optional[bool] = Field(None, description="Rebuild even if embeddings already exist (overwrites them).")

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=1000, description="Chat message")
    filename: Optional[str] = Field(None, description="CSV filename for context")

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str = Field(..., description="AI response")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Source citations")
    query: str = Field(..., description="Original query")

class FileInfo(BaseModel):
    """File information model"""
    filename: str
    size: int
    created_at: float
    file_type: str

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    code: Optional[str] = Field(None, description="Error code")

class SuccessResponse(BaseModel):
    """Generic success response"""
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")

class PaginatedResponse(BaseModel):
    """Paginated response model"""
    results: List[Paper]
    total_results: int
    current_page: int
    total_pages: int
    per_page: int


class ModelComponentStatus(BaseModel):
    """Status for an individual model component"""
    name: str = Field(..., description="Model identifier or name")
    status: str = Field(..., description="Component status: loaded, not_loaded, loading, error, available, unavailable, not_configured, disabled")
    type: str = Field(..., description="Component type: local or remote")
    required: bool = Field(False, description="Whether this component is strictly required")
    details: Optional[str] = Field(None, description="Additional status details")


class ModelsStatus(BaseModel):
    """Overall model status and component breakdown"""
    status: str = Field(..., description="Overall model status: loaded, partial, loading, not_loaded, error")
    components: Dict[str, ModelComponentStatus] = Field(default_factory=dict, description="Component status breakdown")


class SystemStatusResponse(BaseModel):
    """System health and model readiness response"""
    status: str = Field("healthy", description="API health status: healthy, unhealthy")
    api: str = Field("online", description="API connectivity status: online, offline")
    version: str = Field("2.0.0", description="API version")
    timestamp: float = Field(..., description="Current server timestamp")
    models: ModelsStatus = Field(..., description="Model readiness and component breakdown")
    services: Dict[str, str] = Field(default_factory=dict, description="Services summary for backward compatibility")


class AnalysisRequest(BaseModel):
    """Analysis generation request model"""
    filename: str = Field(..., description="CSV filename to analyze")
    top_keywords: int = Field(100, ge=1, le=500, description="Maximum number of keywords to include in the matrix")
    minimum_frequency: int = Field(1, ge=1, description="Minimum frequency required for a keyword to be included")
    refresh: bool = Field(True, description="Rebuild analysis artifacts even if cached versions exist")


class KeywordFrequencyItem(BaseModel):
    """Keyword frequency entry"""
    keyword: str = Field(..., description="Normalized keyword")
    frequency: int = Field(..., ge=0, description="Number of papers containing the keyword")
    percentage: float = Field(..., ge=0, description="Share of papers containing the keyword")


class AnalysisPaperRecord(BaseModel):
    """Normalized paper metadata record used for analysis"""
    paper_id: str
    title: str
    source: str
    year: Optional[str] = None
    doi: Optional[str] = None
    authors: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    abstract: Optional[str] = None
    download_url: Optional[str] = None


class KeywordMatrixRow(BaseModel):
    """Single row in the keyword presence matrix"""
    paper_id: str
    title: str
    source: str
    year: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    values: Dict[str, int] = Field(default_factory=dict)


class CoOccurrenceEdge(BaseModel):
    """Weighted keyword co-occurrence edge"""
    source: str
    target: str
    weight: int = Field(..., ge=0)


class CentralityScore(BaseModel):
    """Centrality values for a keyword node"""
    keyword: str
    degree_centrality: float = Field(..., ge=0)
    closeness_centrality: float = Field(..., ge=0)
    betweenness_centrality: float = Field(..., ge=0)
    eigenvector_centrality: float = Field(..., ge=0)
    clustering_coefficient: float = Field(..., ge=0)


class AnalysisSummary(BaseModel):
    """Summary for generated analysis artifacts"""
    filename: str
    source_file: str
    total_papers: int
    papers_with_keywords: int
    unique_keywords: int
    top_keywords_limit: int
    minimum_frequency: int
    normalized_metadata_file: str
    keyword_frequency_file: str
    keyword_presence_matrix_file: str
    summary_file: str
    generated_at: float
    keyword_frequency: List[KeywordFrequencyItem] = Field(default_factory=list)
    matrix_keywords: List[str] = Field(default_factory=list)
    matrix_rows: int = 0
    matrix_columns: int = 0
    cooccurrence_edges: List[CoOccurrenceEdge] = Field(default_factory=list)
    centrality_scores: List[CentralityScore] = Field(default_factory=list)


class AnalysisSourceInfo(BaseModel):
    """CSV source file available for analysis"""
    filename: str
    size: int
    created_at: float
    paper_count: int = 0
    has_keywords: bool = False


class KeywordMatrixResponse(BaseModel):
    """Keyword matrix response with a preview of the generated matrix"""
    filename: str
    matrix_keywords: List[str] = Field(default_factory=list)
    rows: List[KeywordMatrixRow] = Field(default_factory=list)
    total_rows: int = 0
    total_columns: int = 0
    truncated: bool = False


class CountryNode(BaseModel):
    """Graph node representing a country and its paper count"""
    id: str = Field(..., description="Country identifier")
    label: str = Field(..., description="Country display label")
    iso_a3: Optional[str] = Field(None, description="ISO 3166-1 alpha-3 country code")
    paper_count: int = Field(..., ge=0, description="Number of unique papers associated with this country")


class CountryLink(BaseModel):
    """Graph link representing a collaboration between two countries"""
    source: str = Field(..., description="Source country")
    target: str = Field(..., description="Target country")
    weight: int = Field(..., ge=1, description="Number of papers co-authored by both countries")


class CountryCollaborationGraphResponse(BaseModel):
    """Response model for country collaboration graph data"""
    filename: Optional[str] = Field(None, description="CSV filename analyzed")
    nodes: List[CountryNode] = Field(default_factory=list, description="Graph nodes for countries")
    links: List[CountryLink] = Field(default_factory=list, description="Graph links for country collaborations")
    total_papers: int = Field(0, ge=0, description="Total papers analyzed")
    papers_with_country_data: int = Field(0, ge=0, description="Number of papers with valid country affiliations")
    papers_without_country_data: int = Field(0, ge=0, description="Number of papers lacking usable country affiliations")
    international_papers: int = Field(0, ge=0, description="Number of papers with international collaborations (2+ countries)")
    country_coverage_percentage: float = Field(0.0, ge=0.0, description="Percentage of papers with country data")


class CountryFrequencyItem(BaseModel):
    """Country publication frequency and percentage"""
    country: str = Field(..., description="Country name")
    iso_a3: Optional[str] = Field(None, description="ISO 3166-1 alpha-3 country code")
    frequency: int = Field(..., ge=0, description="Paper count")
    percentage: float = Field(..., ge=0.0, description="Percentage of total papers")


class UnassignedPaperInfo(BaseModel):
    """Information for paper lacking country affiliation data"""
    paper_id: str = Field(..., description="Paper ID or PMID")
    title: str = Field(..., description="Paper title")
    authors: Optional[Union[str, List[str]]] = Field(None, description="Authors")
    source: Optional[str] = Field(None, description="Journal or source")
    year: Optional[str] = Field(None, description="Publication year")


class CountryStatisticsResponse(BaseModel):
    """Response model for country publication statistics endpoint"""
    filename: Optional[str] = Field(None, description="CSV filename analyzed")
    total_papers: int = Field(0, ge=0, description="Total papers analyzed")
    papers_with_country_data: int = Field(0, ge=0, description="Number of papers with valid country affiliations")
    papers_without_country_data: int = Field(0, ge=0, description="Number of papers lacking usable country affiliations")
    unique_countries: int = Field(0, ge=0, description="Number of unique countries detected")
    international_papers: int = Field(0, ge=0, description="Number of papers with international collaborations (2+ countries)")
    country_coverage_percentage: float = Field(0.0, ge=0.0, description="Percentage of papers with country data")
    countries: List[CountryFrequencyItem] = Field(default_factory=list, description="List of countries with paper counts and percentages")
    unassigned_papers: List[UnassignedPaperInfo] = Field(default_factory=list, description="List of papers lacking country data for transparency")


# ---------------------------------------------------------------------------
# Canonical Dataset Normalization & Quality Schemas (Phases 1, 2 & 3)
# ---------------------------------------------------------------------------
from app.services.dataset_normalizer import (
    ColumnMapping,
    NormalizationReport,
    CanonicalPaperRecord,
)
from app.services.dataset_quality import (
    FeatureReadinessStatus,
    FeatureReadiness,
    FieldStatistics,
    DatasetQualityReport,
)


class ExtendedFileUploadResponse(BaseModel):
    """
    Extended response model for CSV file upload including intelligent schema normalization,
    quality score, feature readiness assessment, and vector index status.
    Preserves backward compatibility with legacy {"message": ..., "filename": ...}.
    """
    message: str = Field(..., description="Upload status message")
    filename: str = Field(..., description="Uploaded safe filename")
    encoding: str = Field("utf-8", description="Detected character encoding")
    total_records: int = Field(0, ge=0, description="Total number of paper records in the CSV")
    valid_records: int = Field(0, ge=0, description="Number of unique non-duplicate records")
    duplicate_records: int = Field(0, ge=0, description="Number of duplicate paper records detected")
    overall_quality_score: float = Field(0.0, ge=0.0, le=100.0, description="Overall dataset quality score (0-100)")
    quality_grade: str = Field("Critical", description="Quality grade (Excellent, Good, Fair, Poor, Critical)")
    canonical_fields_detected: List[str] = Field(default_factory=list, description="Canonical fields identified")
    column_mappings: Dict[str, ColumnMapping] = Field(default_factory=dict, description="Resolved column mappings")
    unmapped_columns: List[str] = Field(default_factory=list, description="Custom unmapped column names")
    conflicting_mappings: List[str] = Field(default_factory=list, description="Columns claiming duplicate canonical targets")
    feature_readiness: Dict[str, FeatureReadiness] = Field(default_factory=dict, description="Operational readiness per feature")
    warnings: List[str] = Field(default_factory=list, description="Data hygiene and coverage warnings")
    recommendations: List[str] = Field(default_factory=list, description="Actionable dataset improvement steps")
    index_status: str = Field("not_indexed", description="Vector index status (indexed, not_indexed)")


__all__ = [name for name in dir() if not name.startswith("_")]



