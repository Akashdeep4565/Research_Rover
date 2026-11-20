"""
Modular Dataset Quality Assessment and Feature Readiness Layer for Research Rover.

Evaluates normalized research-paper datasets against measurable quality criteria
and determines the operational readiness of all existing Research Rover features:
- Keyword Frequency & Word Clouds
- Keyword Co-occurrence & Network Centralities
- Country & Affiliation Analysis (2D/3D Maps, International Collaborations)
- Author Analytics & Collaboration
- Research Publication Trends (Timeline)
- Semantic Vector Search & FAISS Indexing
- AI Research Assistant / RAG Chat

Calculates an overall quality score (0 - 100), quality grade, field statistics,
duplicate metrics, and actionable recommendations without mutating source data.
"""

from enum import Enum
import logging
import math
from typing import Any, Dict, List, Optional, Set, Tuple

import pandas as pd
from pydantic import BaseModel, Field

from app.services.dataset_normalizer import (
    CanonicalPaperRecord,
    DatasetNormalizer,
    NormalizationReport,
)

logger = logging.getLogger("research_rover")


# ---------------------------------------------------------------------------
# Enums and Models
# ---------------------------------------------------------------------------

class FeatureReadinessStatus(str, Enum):
    """Operational readiness status for a Research Rover analytical feature."""
    READY = "ready"
    PARTIALLY_READY = "partially_ready"
    NOT_READY = "not_ready"


class FeatureReadiness(BaseModel):
    """Readiness assessment result for a specific Research Rover feature."""
    feature_name: str
    status: FeatureReadinessStatus
    required_fields: List[str] = Field(default_factory=list)
    available_fields: List[str] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)
    coverage_percentage: float = Field(0.0, ge=0.0, le=100.0)
    warnings: List[str] = Field(default_factory=list)
    explanation: str


class FieldStatistics(BaseModel):
    """Detailed completeness and validity statistics for a single canonical field."""
    field_name: str
    total_records: int = 0
    populated_records: int = 0
    missing_records: int = 0
    invalid_records: int = 0
    coverage_percentage: float = Field(0.0, ge=0.0, le=100.0)


class DatasetQualityReport(BaseModel):
    """
    Comprehensive quality and compatibility assessment report for a research-paper dataset.
    Separates general dataset hygiene from individual feature readiness.
    """
    overall_quality_score: float = Field(0.0, ge=0.0, le=100.0)
    quality_grade: str = "Critical"  # Excellent, Good, Fair, Poor, Critical
    total_records: int = 0
    valid_records: int = 0
    duplicate_records: int = 0
    field_statistics: Dict[str, FieldStatistics] = Field(default_factory=dict)
    unmapped_columns: List[str] = Field(default_factory=list)
    feature_readiness: Dict[str, FeatureReadiness] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    normalization_report: Optional[NormalizationReport] = None


# ---------------------------------------------------------------------------
# Dataset Quality & Readiness Assessor
# ---------------------------------------------------------------------------

class DatasetQualityAssessor:
    """
    Evaluates dataset quality and computes feature readiness for Research Rover.
    Works directly with CanonicalPaperRecords produced by DatasetNormalizer.
    """

    # Scoring weights across primary dimensions (Sum = 100 points)
    WEIGHT_TITLE = 25.0
    WEIGHT_ABSTRACT = 20.0
    WEIGHT_KEYWORDS = 15.0
    WEIGHT_AFFILIATIONS = 10.0
    WEIGHT_AUTHORS = 10.0
    WEIGHT_YEAR = 10.0
    WEIGHT_IDENTIFIER = 10.0

    @classmethod
    def _compute_grade(cls, score: float) -> str:
        """Map numerical quality score to a standard grade category."""
        if score >= 90.0:
            return "Excellent"
        if score >= 75.0:
            return "Good"
        if score >= 50.0:
            return "Fair"
        if score >= 25.0:
            return "Poor"
        return "Critical"

    @classmethod
    def assess_field_statistics(
        cls,
        records: List[CanonicalPaperRecord],
        normalization_report: Optional[NormalizationReport] = None,
    ) -> Dict[str, FieldStatistics]:
        """
        Compute population, missing, and invalid counts across all canonical fields.
        Distinguishes missing fields from malformed/invalid inputs.
        """
        n = len(records)
        if n == 0:
            return {}

        fields_to_track = [
            "title",
            "abstract",
            "authors",
            "affiliations",
            "countries",
            "keywords",
            "publication_year",
            "publication_date",
            "journal",
            "doi",
            "pmid",
            "citation_count",
            "download_url",
            "is_open_access",
        ]

        stats: Dict[str, FieldStatistics] = {}

        for field_name in fields_to_track:
            populated = 0
            invalid = 0

            for rec in records:
                val = getattr(rec, field_name, None)

                if field_name == "title":
                    if val and val != "Unknown Title":
                        populated += 1
                    else:
                        pass  # Counted as missing
                elif field_name in ("authors", "affiliations", "countries", "keywords"):
                    if isinstance(val, list) and len(val) > 0:
                        populated += 1
                elif field_name == "publication_year":
                    if val is not None and isinstance(val, int) and 1800 <= val <= 2035:
                        populated += 1
                    else:
                        # Check if raw_data had a value that failed parsing
                        raw_year = cls._find_raw_value(rec.raw_data, ["year", "publication_year", "year_published", "pub_year"])
                        if raw_year and str(raw_year).strip() and str(raw_year).strip().lower() not in ("none", "nan", "null", "n/a", ""):
                            invalid += 1
                elif field_name == "doi":
                    if val is not None and str(val).startswith("10.") and "/" in str(val):
                        populated += 1
                    else:
                        raw_doi = cls._find_raw_value(rec.raw_data, ["doi", "digital_object_identifier", "document_doi"])
                        if raw_doi and str(raw_doi).strip() and str(raw_doi).strip().lower() not in ("none", "nan", "null", "n/a", ""):
                            invalid += 1
                elif field_name == "citation_count":
                    if val is not None and isinstance(val, int) and val >= 0:
                        populated += 1
                    else:
                        raw_cite = cls._find_raw_value(rec.raw_data, ["citations", "citation_count", "cited_by", "times_cited"])
                        if raw_cite and str(raw_cite).strip() and str(raw_cite).strip().lower() not in ("none", "nan", "null", "n/a", ""):
                            invalid += 1
                else:
                    if val is not None and str(val).strip() and str(val).strip().lower() not in ("none", "nan", "null", "n/a", ""):
                        populated += 1

            missing = n - populated
            coverage = round((populated / n) * 100.0, 1)

            stats[field_name] = FieldStatistics(
                field_name=field_name,
                total_records=n,
                populated_records=populated,
                missing_records=missing,
                invalid_records=invalid,
                coverage_percentage=coverage,
            )

        return stats

    @staticmethod
    def _find_raw_value(raw_data: Dict[str, Any], candidate_keys: List[str]) -> Optional[Any]:
        """Locate raw cell value by loosely checking candidate column keys."""
        if not raw_data:
            return None
        lower_map = {str(k).lower().replace(" ", "_").replace("-", "_"): v for k, v in raw_data.items()}
        for ck in candidate_keys:
            if ck in lower_map:
                return lower_map[ck]
        return None

    @classmethod
    def calculate_quality_score(
        cls,
        records: List[CanonicalPaperRecord],
        field_stats: Dict[str, FieldStatistics],
        duplicate_count: int = 0,
    ) -> float:
        """
        Calculate overall dataset quality score (0.0 - 100.0).

        Scoring Formula:
        Base = 25*(Title%) + 20*(Abstract%) + 15*(Keywords%) + 10*(Affil%) + 10*(Authors%) + 10*(Year%) + 10*(ID%)
        Deductions:
          - Duplicate Penalty: up to -10 pts proportional to duplicate rate.
          - Invalid Values Penalty: up to -5 pts for malformed/corrupted cells.
        Scaling:
          - Small Sample Damping: datasets with N < 5 are scaled by (N / 5) to prevent
            1-paper datasets from obtaining a 100/100 'Excellent' score.
        """
        n = len(records)
        if n == 0:
            return 0.0

        def get_cov(field_name: str) -> float:
            stat = field_stats.get(field_name)
            return (stat.populated_records / n) if stat else 0.0

        cov_title = get_cov("title")
        cov_abstract = get_cov("abstract")
        cov_keywords = get_cov("keywords")
        cov_authors = get_cov("authors")

        # Affiliations: check either affiliations or countries populated
        affil_stat = field_stats.get("affiliations")
        country_stat = field_stats.get("countries")
        affil_pop = max(
            affil_stat.populated_records if affil_stat else 0,
            country_stat.populated_records if country_stat else 0,
        )
        cov_affil = affil_pop / n

        cov_year = get_cov("publication_year")

        # Identifiers: check DOI or PMID presence
        doi_stat = field_stats.get("doi")
        pmid_stat = field_stats.get("pmid")
        id_pop = max(
            doi_stat.populated_records if doi_stat else 0,
            pmid_stat.populated_records if pmid_stat else 0,
        )
        cov_id = id_pop / n

        # Base weighted score (0 - 100)
        base_score = (
            cls.WEIGHT_TITLE * cov_title
            + cls.WEIGHT_ABSTRACT * cov_abstract
            + cls.WEIGHT_KEYWORDS * cov_keywords
            + cls.WEIGHT_AFFILIATIONS * cov_affil
            + cls.WEIGHT_AUTHORS * cov_authors
            + cls.WEIGHT_YEAR * cov_year
            + cls.WEIGHT_IDENTIFIER * cov_id
        )

        # 1. Duplicate penalty (up to 10 points)
        dup_rate = duplicate_count / n
        dup_penalty = min(10.0, dup_rate * 20.0)

        # 2. Invalid entries penalty (up to 5 points)
        total_invalids = sum(s.invalid_records for s in field_stats.values())
        invalid_rate = total_invalids / (n * max(1, len(field_stats)))
        invalid_penalty = min(5.0, invalid_rate * 25.0)

        # Net score before damping
        net_score = max(0.0, base_score - dup_penalty - invalid_penalty)

        # 3. Small sample damping (N < 5)
        damping = min(1.0, n / 5.0)
        final_score = net_score * damping

        return round(max(0.0, min(100.0, final_score)), 1)

    @classmethod
    def evaluate_feature_readiness(
        cls,
        records: List[CanonicalPaperRecord],
        field_stats: Dict[str, FieldStatistics],
    ) -> Dict[str, FeatureReadiness]:
        """
        Evaluate readiness of each individual Research Rover feature based on actual
        backend service logic and minimum required fields.
        """
        n = len(records)
        readiness: Dict[str, FeatureReadiness] = {}

        # Helper to get populated count
        def pop_cnt(field_name: str) -> int:
            st = field_stats.get(field_name)
            return st.populated_records if st else 0

        # Helper to get coverage %
        def cov_pct(field_name: str) -> float:
            st = field_stats.get(field_name)
            return st.coverage_percentage if st else 0.0

        if n == 0:
            # All features not ready when dataset is empty
            features = [
                ("keyword_analysis", "Keyword Frequency & Word Clouds", ["keywords"]),
                ("cooccurrence_analysis", "Keyword Co-occurrence & Network Centralities", ["keywords"]),
                ("country_analysis", "Country Distribution & Collaboration Networks", ["affiliations"]),
                ("author_analysis", "Author Analytics & Collaboration", ["authors"]),
                ("trend_analysis", "Research Publication Trends", ["publication_year"]),
                ("semantic_search", "Semantic Vector Search & Indexing", ["title", "abstract"]),
                ("ai_chat_rag", "AI Research Assistant (RAG Chat)", ["title", "abstract"]),
            ]
            for fid, fname, reqs in features:
                readiness[fid] = FeatureReadiness(
                    feature_name=fname,
                    status=FeatureReadinessStatus.NOT_READY,
                    required_fields=reqs,
                    available_fields=[],
                    missing_fields=reqs,
                    coverage_percentage=0.0,
                    warnings=["Dataset contains 0 records."],
                    explanation="Dataset is empty. No records available for analysis.",
                )
            return readiness

        # -------------------------------------------------------------------
        # 1. Keyword Analysis (Frequency, Word Cloud, Presences)
        # -------------------------------------------------------------------
        kw_pop = pop_cnt("keywords")
        kw_cov = cov_pct("keywords")
        all_unique_kws: Set[str] = set()
        for r in records:
            all_unique_kws.update(r.keywords)

        if kw_pop == 0:
            readiness["keyword_analysis"] = FeatureReadiness(
                feature_name="Keyword Frequency & Word Clouds",
                status=FeatureReadinessStatus.NOT_READY,
                required_fields=["keywords"],
                available_fields=[],
                missing_fields=["keywords"],
                coverage_percentage=0.0,
                warnings=["No keyword data found in dataset."],
                explanation="None of the papers contain keywords. Keyword frequency tables and word clouds cannot be generated.",
            )
        elif kw_cov >= 50.0 and len(all_unique_kws) >= 3:
            readiness["keyword_analysis"] = FeatureReadiness(
                feature_name="Keyword Frequency & Word Clouds",
                status=FeatureReadinessStatus.READY,
                required_fields=["keywords"],
                available_fields=["keywords"],
                missing_fields=[],
                coverage_percentage=kw_cov,
                warnings=[],
                explanation=f"{kw_pop}/{n} papers ({kw_cov}%) contain keyword metadata with {len(all_unique_kws)} unique terms. Fully operational.",
            )
        else:
            readiness["keyword_analysis"] = FeatureReadiness(
                feature_name="Keyword Frequency & Word Clouds",
                status=FeatureReadinessStatus.PARTIALLY_READY,
                required_fields=["keywords"],
                available_fields=["keywords"],
                missing_fields=[],
                coverage_percentage=kw_cov,
                warnings=[f"Low keyword coverage ({kw_cov}%) or limited unique terms ({len(all_unique_kws)})."],
                explanation=f"Keyword analysis will operate, but frequency metrics may be skewed because {n - kw_pop} papers lack keywords.",
            )

        # -------------------------------------------------------------------
        # 2. Keyword Co-occurrence & Network Centralities (Degrees, Betweenness)
        # -------------------------------------------------------------------
        multi_kw_papers = sum(1 for r in records if len(r.keywords) >= 2)
        multi_kw_pct = round((multi_kw_papers / n) * 100.0, 1)

        if multi_kw_papers < 2:
            readiness["cooccurrence_analysis"] = FeatureReadiness(
                feature_name="Keyword Co-occurrence & Network Centralities",
                status=FeatureReadinessStatus.NOT_READY,
                required_fields=["keywords"],
                available_fields=["keywords"] if kw_pop > 0 else [],
                missing_fields=[] if kw_pop > 0 else ["keywords"],
                coverage_percentage=multi_kw_pct,
                warnings=["Fewer than 2 papers contain multi-keyword combinations."],
                explanation="Network co-occurrence and centrality scores require papers with at least 2 keywords each to compute graph edges.",
            )
        elif multi_kw_papers >= 5 and multi_kw_pct >= 40.0:
            readiness["cooccurrence_analysis"] = FeatureReadiness(
                feature_name="Keyword Co-occurrence & Network Centralities",
                status=FeatureReadinessStatus.READY,
                required_fields=["keywords"],
                available_fields=["keywords"],
                missing_fields=[],
                coverage_percentage=multi_kw_pct,
                warnings=[],
                explanation=f"{multi_kw_papers}/{n} papers ({multi_kw_pct}%) have 2+ keywords. Co-occurrence graph and centrality algorithms fully operational.",
            )
        else:
            readiness["cooccurrence_analysis"] = FeatureReadiness(
                feature_name="Keyword Co-occurrence & Network Centralities",
                status=FeatureReadinessStatus.PARTIALLY_READY,
                required_fields=["keywords"],
                available_fields=["keywords"],
                missing_fields=[],
                coverage_percentage=multi_kw_pct,
                warnings=[f"Sparse co-occurrence network: only {multi_kw_papers} papers contain multiple keywords."],
                explanation="Co-occurrence matrix will be sparse. Network centrality metrics may show disconnected subgraphs.",
            )

        # -------------------------------------------------------------------
        # 3. Country & Affiliation Analysis (2D Map, 3D Globe, Collaboration)
        # -------------------------------------------------------------------
        affil_pop = pop_cnt("affiliations")
        country_pop = pop_cnt("countries")
        geo_pop = sum(1 for r in records if len(r.affiliations) > 0 or len(r.countries) > 0)
        geo_cov = round((geo_pop / n) * 100.0, 1)

        if geo_pop == 0:
            readiness["country_analysis"] = FeatureReadiness(
                feature_name="Country Distribution & Collaboration Networks",
                status=FeatureReadinessStatus.NOT_READY,
                required_fields=["affiliations"],
                available_fields=[],
                missing_fields=["affiliations"],
                coverage_percentage=0.0,
                warnings=["No author affiliation or country data present."],
                explanation="Affiliation addresses are missing. World map, 3D globe, and international collaboration networks cannot be rendered.",
            )
        elif geo_cov >= 40.0:
            readiness["country_analysis"] = FeatureReadiness(
                feature_name="Country Distribution & Collaboration Networks",
                status=FeatureReadinessStatus.READY,
                required_fields=["affiliations"],
                available_fields=["affiliations"] if affil_pop else ["countries"],
                missing_fields=[],
                coverage_percentage=geo_cov,
                warnings=[],
                explanation=f"{geo_pop}/{n} papers ({geo_cov}%) contain institutional or country affiliations. Geoparsing and collaboration graphs fully operational.",
            )
        else:
            readiness["country_analysis"] = FeatureReadiness(
                feature_name="Country Distribution & Collaboration Networks",
                status=FeatureReadinessStatus.PARTIALLY_READY,
                required_fields=["affiliations"],
                available_fields=["affiliations"] if affil_pop else ["countries"],
                missing_fields=[],
                coverage_percentage=geo_cov,
                warnings=[f"Moderate affiliation coverage ({geo_cov}%). {n - geo_pop} papers lack location metadata."],
                explanation="Country extraction will operate on available records, but unassigned papers table will contain unmapped rows.",
            )

        # -------------------------------------------------------------------
        # 4. Author Analysis & Collaboration
        # -------------------------------------------------------------------
        author_pop = pop_cnt("authors")
        author_cov = cov_pct("authors")

        if author_pop == 0:
            readiness["author_analysis"] = FeatureReadiness(
                feature_name="Author Analytics & Collaboration",
                status=FeatureReadinessStatus.NOT_READY,
                required_fields=["authors"],
                available_fields=[],
                missing_fields=["authors"],
                coverage_percentage=0.0,
                warnings=["No author names present in dataset."],
                explanation="Author metadata is absent. Author frequency, co-authorship lists, and researcher rankings cannot be computed.",
            )
        elif author_cov >= 50.0:
            readiness["author_analysis"] = FeatureReadiness(
                feature_name="Author Analytics & Collaboration",
                status=FeatureReadinessStatus.READY,
                required_fields=["authors"],
                available_fields=["authors"],
                missing_fields=[],
                coverage_percentage=author_cov,
                warnings=[],
                explanation=f"{author_pop}/{n} papers ({author_cov}%) have author metadata. Author analytics fully operational.",
            )
        else:
            readiness["author_analysis"] = FeatureReadiness(
                feature_name="Author Analytics & Collaboration",
                status=FeatureReadinessStatus.PARTIALLY_READY,
                required_fields=["authors"],
                available_fields=["authors"],
                missing_fields=[],
                coverage_percentage=author_cov,
                warnings=[f"Low author coverage ({author_cov}%)."],
                explanation="Author analysis will only reflect the subset of papers containing author records.",
            )

        # -------------------------------------------------------------------
        # 5. Publication Trends (Timeline Analysis)
        # -------------------------------------------------------------------
        year_pop = pop_cnt("publication_year")
        year_cov = cov_pct("publication_year")
        distinct_years = {r.publication_year for r in records if r.publication_year is not None}

        if year_pop == 0:
            readiness["trend_analysis"] = FeatureReadiness(
                feature_name="Research Publication Trends",
                status=FeatureReadinessStatus.NOT_READY,
                required_fields=["publication_year"],
                available_fields=[],
                missing_fields=["publication_year"],
                coverage_percentage=0.0,
                warnings=["No valid publication years found in dataset."],
                explanation="Publication years are missing or unparseable. Annual publication trends and temporal graphs cannot be generated.",
            )
        elif year_cov >= 50.0 and len(distinct_years) >= 2:
            readiness["trend_analysis"] = FeatureReadiness(
                feature_name="Research Publication Trends",
                status=FeatureReadinessStatus.READY,
                required_fields=["publication_year"],
                available_fields=["publication_year"],
                missing_fields=[],
                coverage_percentage=year_cov,
                warnings=[],
                explanation=f"{year_pop}/{n} papers ({year_cov}%) have valid years spanning {min(distinct_years)} - {max(distinct_years)}. Timeline charts fully operational.",
            )
        else:
            readiness["trend_analysis"] = FeatureReadiness(
                feature_name="Research Publication Trends",
                status=FeatureReadinessStatus.PARTIALLY_READY,
                required_fields=["publication_year"],
                available_fields=["publication_year"],
                missing_fields=[],
                coverage_percentage=year_cov,
                warnings=[f"Single publication year ({list(distinct_years)}) or low year coverage ({year_cov}%)."],
                explanation="Trend charts can display available data, but temporal trajectory analysis requires multiple years of coverage.",
            )

        # -------------------------------------------------------------------
        # 6. Semantic Vector Search & Indexing (HDBSCAN + FAISS)
        # -------------------------------------------------------------------
        title_pop = pop_cnt("title")
        abstract_pop = sum(1 for r in records if r.abstract and len(r.abstract.strip()) >= 20)
        abstract_cov = round((abstract_pop / n) * 100.0, 1)

        dl_pop = pop_cnt("download_url")

        if abstract_pop == 0 and dl_pop == 0:
            readiness["semantic_search"] = FeatureReadiness(
                feature_name="Semantic Vector Search & Indexing",
                status=FeatureReadinessStatus.NOT_READY,
                required_fields=["abstract"],
                available_fields=["title"] if title_pop else [],
                missing_fields=["abstract"],
                coverage_percentage=0.0,
                warnings=["No paper abstracts or downloadable URLs available for text embedding."],
                explanation="Semantic search requires paper text (abstracts or full-text URLs) to generate sentence embeddings and build FAISS vector indices.",
            )
        elif abstract_cov >= 50.0 and title_pop > 0:
            readiness["semantic_search"] = FeatureReadiness(
                feature_name="Semantic Vector Search & Indexing",
                status=FeatureReadinessStatus.READY,
                required_fields=["title", "abstract"],
                available_fields=["title", "abstract"],
                missing_fields=[],
                coverage_percentage=abstract_cov,
                warnings=[],
                explanation=f"{abstract_pop}/{n} papers ({abstract_cov}%) contain multi-sentence abstracts suitable for HDBSCAN chunking and FAISS indexing.",
            )
        else:
            readiness["semantic_search"] = FeatureReadiness(
                feature_name="Semantic Vector Search & Indexing",
                status=FeatureReadinessStatus.PARTIALLY_READY,
                required_fields=["title", "abstract"],
                available_fields=["title"] if title_pop else [] + (["abstract"] if abstract_pop else []),
                missing_fields=["abstract"] if abstract_pop == 0 else [],
                coverage_percentage=abstract_cov,
                warnings=[f"Limited abstract coverage ({abstract_cov}%). Papers lacking abstracts will be excluded from vector search."],
                explanation="Vector indexing can proceed on available abstracts or via web scraping, but coverage is incomplete.",
            )

        # -------------------------------------------------------------------
        # 7. AI Research Assistant (RAG Chat)
        # -------------------------------------------------------------------
        sem_status = readiness["semantic_search"].status
        doi_pop = pop_cnt("doi")

        if sem_status == FeatureReadinessStatus.NOT_READY:
            readiness["ai_chat_rag"] = FeatureReadiness(
                feature_name="AI Research Assistant (RAG Chat)",
                status=FeatureReadinessStatus.NOT_READY,
                required_fields=["abstract", "title"],
                available_fields=["title"] if title_pop else [],
                missing_fields=["abstract"],
                coverage_percentage=0.0,
                warnings=["No text content available to index for document-grounded RAG answers."],
                explanation="Without abstract or full text embeddings, AI Chat cannot retrieve paper context and would produce ungrounded generic answers.",
            )
        elif sem_status == FeatureReadinessStatus.READY:
            rag_warnings = []
            if doi_pop < (n * 0.5):
                rag_warnings.append("Many papers lack DOIs. Chat answers will be grounded in text, but direct citation DOI links may be missing.")

            readiness["ai_chat_rag"] = FeatureReadiness(
                feature_name="AI Research Assistant (RAG Chat)",
                status=FeatureReadinessStatus.READY,
                required_fields=["title", "abstract"],
                available_fields=["title", "abstract"] + (["doi"] if doi_pop else []),
                missing_fields=[],
                coverage_percentage=abstract_cov,
                warnings=rag_warnings,
                explanation="Papers have sufficient textual depth for semantic chunking and grounded multi-query RAG generation with citations.",
            )
        else:
            readiness["ai_chat_rag"] = FeatureReadiness(
                feature_name="AI Research Assistant (RAG Chat)",
                status=FeatureReadinessStatus.PARTIALLY_READY,
                required_fields=["title", "abstract"],
                available_fields=["title"] if title_pop else [] + (["abstract"] if abstract_pop else []),
                missing_fields=["abstract"] if abstract_pop == 0 else [],
                coverage_percentage=abstract_cov,
                warnings=[f"Partial paper context available ({abstract_cov}%). Questions about papers without abstracts cannot be answered from data."],
                explanation="RAG chat will function for papers with indexed text, but will lack context for unindexed records.",
            )

        return readiness

    @classmethod
    def generate_recommendations(
        cls,
        field_stats: Dict[str, FieldStatistics],
        readiness: Dict[str, FeatureReadiness],
        quality_score: float,
        duplicate_count: int,
        unmapped_cols: List[str],
    ) -> List[str]:
        """Generate human-readable, actionable recommendations to improve dataset quality."""
        recs: List[str] = []

        if duplicate_count > 0:
            recs.append(
                f"Dataset contains {duplicate_count} duplicate paper records. Consider deduplicating by DOI/PMID to prevent overcounting in frequency analyses."
            )

        # Check critical fields
        title_stat = field_stats.get("title")
        if title_stat and title_stat.coverage_percentage < 100.0:
            recs.append(
                f"Missing {title_stat.missing_records} paper titles. Ensure every record contains an identifiable title header."
            )

        abstract_stat = field_stats.get("abstract")
        if abstract_stat and abstract_stat.coverage_percentage < 50.0:
            recs.append(
                f"Abstract coverage is low ({abstract_stat.coverage_percentage}%). Adding abstracts unlocks semantic search, HDBSCAN clustering, and AI RAG chat."
            )

        kw_stat = field_stats.get("keywords")
        if kw_stat and kw_stat.coverage_percentage < 50.0:
            recs.append(
                f"Keywords coverage is {kw_stat.coverage_percentage}%. Adding semicolon-delimited keywords unlocks keyword frequency and network co-occurrence graphs."
            )

        affil_stat = field_stats.get("affiliations")
        if affil_stat and affil_stat.coverage_percentage < 40.0:
            recs.append(
                f"Affiliations coverage is {affil_stat.coverage_percentage}%. Include institution or country addresses to render 2D/3D country collaboration maps."
            )

        year_stat = field_stats.get("publication_year")
        if year_stat and year_stat.invalid_records > 0:
            recs.append(
                f"Detected {year_stat.invalid_records} invalid publication year entries. Format years as clean 4-digit integers (e.g. 2023)."
            )

        if unmapped_cols:
            recs.append(
                f"Detected {len(unmapped_cols)} unmapped columns ({', '.join(unmapped_cols[:3])}{'...' if len(unmapped_cols) > 3 else ''}). Use custom column mappings to associate them with canonical fields."
            )

        if quality_score >= 85.0 and not recs:
            recs.append("Dataset meets all quality benchmarks. All Research Rover analytical features are fully operational.")

        return recs

    # -----------------------------------------------------------------------
    # Main Public Assessment Methods
    # -----------------------------------------------------------------------

    def assess(
        self,
        records: List[CanonicalPaperRecord],
        normalization_report: Optional[NormalizationReport] = None,
    ) -> DatasetQualityReport:
        """
        Perform complete quality assessment and feature readiness evaluation on normalized records.
        """
        n = len(records)
        duplicate_count = sum(1 for r in records if r.is_duplicate)
        valid_count = n - duplicate_count

        field_stats = self.assess_field_statistics(records, normalization_report)
        score = self.calculate_quality_score(records, field_stats, duplicate_count)
        grade = self._compute_grade(score)
        readiness = self.evaluate_feature_readiness(records, field_stats)

        # Unmapped columns from normalization report
        unmapped_cols: List[str] = []
        if normalization_report and normalization_report.mappings:
            unmapped_cols = [
                col for col, m in normalization_report.mappings.items() if m.status == "unmapped"
            ]

        recommendations = self.generate_recommendations(
            field_stats,
            readiness,
            score,
            duplicate_count,
            unmapped_cols,
        )

        return DatasetQualityReport(
            overall_quality_score=score,
            quality_grade=grade,
            total_records=n,
            valid_records=valid_count,
            duplicate_records=duplicate_count,
            field_statistics=field_stats,
            unmapped_columns=unmapped_cols,
            feature_readiness=readiness,
            recommendations=recommendations,
            normalization_report=normalization_report,
        )

    def assess_dataframe(
        self,
        df: pd.DataFrame,
        custom_mappings: Optional[Dict[str, str]] = None,
        fuzzy_threshold: float = 0.85,
    ) -> DatasetQualityReport:
        """
        Convenience end-to-end evaluation: normalizes a DataFrame and assesses its quality.
        Does NOT mutate the input DataFrame.
        """
        normalizer = DatasetNormalizer(fuzzy_threshold=fuzzy_threshold)
        records, norm_report = normalizer.normalize_dataframe(df, custom_mappings=custom_mappings)
        return self.assess(records, normalization_report=norm_report)
