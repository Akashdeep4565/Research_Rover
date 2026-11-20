"""
Standalone Canonical Dataset Normalization Engine for Research Rover.

Provides intelligent column detection, multi-tier schema mapping (exact,
deterministic alias, normalized header, and fuzzy Levenshtein), non-destructive
canonical record transformation, conflict reporting, and duplicate tracking
for research-paper datasets.

Supports bibliographic exports from PubMed, Scopus, Web of Science, OpenAlex,
arXiv, Crossref, and custom CSV schemas without modifying source files.
"""

import ast
import difflib
import json
import logging
import math
import re
import unicodedata
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pandas as pd
from pydantic import BaseModel, Field

logger = logging.getLogger("research_rover")

# ---------------------------------------------------------------------------
# Canonical Fields Specification
# ---------------------------------------------------------------------------

CANONICAL_FIELDS: Set[str] = {
    "paper_id",
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
    "pmcid",
    "openalex_id",
    "citation_count",
    "publication_type",
    "url",
    "download_url",
    "is_open_access",
    "raw_data",
}

# ---------------------------------------------------------------------------
# Comprehensive Aliases Dictionary
# Keys are sanitized (lowercase, stripped punctuation, normalized spaces).
# Generic 'id' is intentionally omitted from keywords and scalar fields.
# ---------------------------------------------------------------------------

CANONICAL_ALIASES: Dict[str, Set[str]] = {
    "title": {
        "title",
        "article title",
        "paper title",
        "document title",
        "item title",
        "entry title",
        "display name",
        "heading",
        "ti",
        "paper name",
        "article name",
        "work title",
        "publication title article",
    },
    "abstract": {
        "abstract",
        "summary",
        "description",
        "paper abstract",
        "ab",
        "abstract note",
        "synopsis",
        "executive summary",
        "brief summary",
        "article abstract",
    },
    "authors": {
        "authors",
        "author",
        "author names",
        "researchers",
        "creators",
        "contributors",
        "authorships",
        "investigators",
        "au",
        "first author",
        "author s",
        "author list",
        "author full names",
        "authors full names",
        "full author names",
    },
    "affiliations": {
        "affiliations",
        "affiliation",
        "addresses",
        "author address",
        "author addresses",
        "institutions",
        "institution",
        "author affiliations",
        "author affiliation",
        "organization",
        "organizations",
        "c1",
        "affiliation name",
        "author organization",
        "corporate authors",
    },
    "countries": {
        "countries",
        "country",
        "author countries",
        "author country",
        "affil country",
        "geo country",
        "country of publication",
        "countries of publication",
    },
    "keywords": {
        "keywords",
        "author keywords",
        "index keywords",
        "mesh terms",
        "mesh",
        "keywords plus",
        "subject terms",
        "tags",
        "concepts",
        "topics",
        "controlled terms",
        "descriptors",
        "subject headings",
        "all keywords",
        "research topics",
        "subject tags",
    },
    "publication_year": {
        "publication year",
        "year published",
        "year",
        "pub year",
        "py",
        "publication date year",
        "release year",
        "date year",
        "pub yr",
        "pubyear",
        "article year",
        "document year",
    },
    "publication_date": {
        "publication date",
        "published date",
        "pub date",
        "pd",
        "release date",
        "issued date",
        "date of publication",
        "issue date",
        "online publication date",
        "epub date",
    },
    "journal": {
        "journal",
        "source",
        "source title",
        "journal name",
        "publication title",
        "journal book",
        "book title",
        "venue",
        "publisher",
        "so",
        "series",
        "conference",
        "conference title",
        "periodical",
        "container title",
        "primary location source display name",
    },
    "doi": {
        "doi",
        "di",
        "digital object identifier",
        "document doi",
        "article doi",
        "electronic doi",
        "doi link",
        "doi identifier",
        "doi id",
        "identifier doi",
    },
    "pmid": {
        "pmid",
        "pubmed id",
        "pm id",
        "pubmed identifier",
        "ncbi id",
        "medline pmid",
    },
    "pmcid": {
        "pmcid",
        "pmc id",
        "pmc",
        "pubmed central id",
    },
    "openalex_id": {
        "openalex id",
        "openalex",
        "open alex id",
        "work id",
        "openalex work id",
    },
    "citation_count": {
        "citation count",
        "cited by",
        "citations",
        "times cited",
        "times cited wos core",
        "times cited all databases",
        "tc",
        "citation num",
        "cited by count",
        "num citations",
        "total citations",
        "cited count",
    },
    "publication_type": {
        "publication type",
        "publication types",
        "document type",
        "doc type",
        "pt",
        "dt",
        "item type",
        "article type",
        "entry type",
        "work type",
    },
    "url": {
        "url",
        "link",
        "paper url",
        "landing page url",
        "web url",
        "item url",
        "source url",
        "view url",
        "article url",
    },
    "download_url": {
        "download url",
        "pdf url",
        "pdf link",
        "fulltext url",
        "full text url",
        "fulltext link",
        "download link",
        "pdf",
        "direct pdf",
        "open access pdf",
    },
    "is_open_access": {
        "is open access",
        "is oa",
        "open access",
        "oa",
        "oa status",
        "open access status",
    },
    "paper_id": {
        "paper id",
        "article id",
        "record id",
        "unique id",
        "ut unique wos id",
        "wos id",
        "ut",
        "accession number",
        "entry id",
    },
}

# Inverted lookup: sanitized alias -> canonical field name
_ALIAS_TO_CANONICAL: Dict[str, str] = {}
for canonical, aliases in CANONICAL_ALIASES.items():
    _ALIAS_TO_CANONICAL[canonical.lower().strip()] = canonical
    _ALIAS_TO_CANONICAL[canonical.replace("_", " ").lower().strip()] = canonical
    for alias in aliases:
        _ALIAS_TO_CANONICAL[alias.lower().strip()] = canonical
        s_alias = re.sub(r"[^\w\s]|_", " ", alias).strip().lower()
        s_alias = re.sub(r"\s+", " ", s_alias)
        _ALIAS_TO_CANONICAL[s_alias] = canonical


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class ColumnMapping(BaseModel):
    """Details of a single source-to-canonical column mapping."""
    original_column: str
    canonical_field: Optional[str] = None
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    matching_method: str = "unmatched"  # exact_canonical, deterministic_alias, normalized_alias, fuzzy_match, manual_override, unmatched
    status: str = "unmapped"            # matched, conflict, uncertain, unmapped
    details: Optional[str] = None


class NormalizationReport(BaseModel):
    """Summary of the dataset schema normalization results and conflicts."""
    total_columns: int = 0
    mapped_columns: int = 0
    unmapped_columns: int = 0
    uncertain_columns: int = 0
    conflicts: List[str] = Field(default_factory=list)
    mappings: Dict[str, ColumnMapping] = Field(default_factory=dict)
    total_records: int = 0
    valid_records: int = 0
    duplicate_records: int = 0


class CanonicalPaperRecord(BaseModel):
    """
    Standardized internal representation of a single research paper record.
    Preserves all original source attributes in raw_data and any conflicting
    scalar column values in conflicting_values.
    """
    record_id: str = "record_unknown"
    paper_id: str = "unknown_paper"
    is_duplicate: bool = False
    duplicate_of: Optional[str] = None
    title: str = "Unknown Title"
    abstract: Optional[str] = None
    authors: List[str] = Field(default_factory=list)
    affiliations: List[str] = Field(default_factory=list)
    countries: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    publication_year: Optional[int] = None
    publication_date: Optional[str] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    pmcid: Optional[str] = None
    openalex_id: Optional[str] = None
    citation_count: Optional[int] = None
    publication_type: Optional[str] = None
    url: Optional[str] = None
    download_url: Optional[str] = None
    is_open_access: Optional[bool] = None
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    conflicting_values: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Normalization Engine
# ---------------------------------------------------------------------------

class DatasetNormalizer:
    """
    Intelligent Column Detection and Schema Normalization Engine.
    Works independently of downstream services and does not mutate source data.
    """

    def __init__(self, fuzzy_threshold: float = 0.85):
        """
        Initialize normalizer.
        :param fuzzy_threshold: Minimum SequenceMatcher similarity ratio for fuzzy matching (0.0 - 1.0).
        """
        self.fuzzy_threshold = fuzzy_threshold

    @staticmethod
    def sanitize_header(header: str) -> str:
        """
        Normalize a raw header string for resilient alias matching:
        - Unicode normalize (NFKD)
        - Lowercase & strip
        - Replace punctuation, underscores, and separators (_, -, /, ., :, ;, etc.) with spaces
        - Collapse multiple spaces into single space
        """
        if not header:
            return ""
        text = unicodedata.normalize("NFKD", str(header)).strip().lower()
        # Replace underscores, hyphens, and any non-alphanumeric character with space
        text = re.sub(r"[^\w\s]|_", " ", text)
        # Collapse whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def identify_column(self, raw_column: str) -> ColumnMapping:
        """
        Identify the canonical field for a single column header through tiered matching:
        Stage 1: Exact canonical field matching.
        Stage 2: Deterministic alias matching.
        Stage 3: Normalized header matching.
        Stage 4: Guarded fuzzy matching via difflib.
        Stage 5: Flag ambiguous or low-margin fuzzy matches as uncertain.
        """
        col_str = str(raw_column).strip()
        if not col_str:
            return ColumnMapping(
                original_column=raw_column,
                canonical_field=None,
                confidence=0.0,
                matching_method="unmatched",
                status="unmapped",
                details="Empty column header",
            )

        # Stage 1: Exact canonical match (case-insensitive)
        lower_raw = col_str.lower()
        if lower_raw in CANONICAL_FIELDS:
            return ColumnMapping(
                original_column=raw_column,
                canonical_field=lower_raw,
                confidence=1.0,
                matching_method="exact_canonical",
                status="matched",
                details=f"Exact match to canonical field '{lower_raw}'",
            )

        # Stage 2 & 3: Sanitized alias matching
        sanitized = self.sanitize_header(col_str)
        if sanitized in _ALIAS_TO_CANONICAL:
            target = _ALIAS_TO_CANONICAL[sanitized]
            return ColumnMapping(
                original_column=raw_column,
                canonical_field=target,
                confidence=1.0 if sanitized == lower_raw else 0.98,
                matching_method="deterministic_alias" if sanitized == lower_raw else "normalized_alias",
                status="matched",
                details=f"Matched alias '{sanitized}' to canonical '{target}'",
            )

        # Stage 4: Guarded Fuzzy Matching with SequenceMatcher against known aliases
        # Guard: Do not fuzzy match short abbreviations (length < 4) to avoid false matches (e.g. 'id' != 'di')
        if len(sanitized) >= 4:
            fuzzy_candidates: List[Tuple[float, str, str]] = []
            for alias, canonical_target in _ALIAS_TO_CANONICAL.items():
                if abs(len(sanitized) - len(alias)) > 6:
                    continue
                ratio = difflib.SequenceMatcher(None, sanitized, alias).ratio()
                if ratio >= self.fuzzy_threshold:
                    fuzzy_candidates.append((ratio, canonical_target, alias))

            if fuzzy_candidates:
                # Sort descending by similarity ratio
                fuzzy_candidates.sort(key=lambda x: x[0], reverse=True)
                best_ratio, best_target, best_alias = fuzzy_candidates[0]

                # Check for competing targets within a 0.08 margin
                competing_targets = [c for c in fuzzy_candidates[1:] if c[1] != best_target]
                is_ambiguous = False
                competing_target_name = None
                if competing_targets:
                    second_ratio, second_target, _ = competing_targets[0]
                    if (best_ratio - second_ratio) < 0.08:
                        is_ambiguous = True
                        competing_target_name = second_target

                if is_ambiguous:
                    # Flag ambiguous match for manual confirmation
                    return ColumnMapping(
                        original_column=raw_column,
                        canonical_field=best_target,
                        confidence=round(best_ratio, 3),
                        matching_method="fuzzy_match",
                        status="uncertain",
                        details=f"Ambiguous fuzzy match: '{best_target}' ({best_ratio:.2f}) vs '{competing_target_name}'. Requires manual confirmation.",
                    )
                elif best_ratio >= 0.92:
                    # High-confidence typo correction (e.g., 'Articel Title' -> 'title')
                    return ColumnMapping(
                        original_column=raw_column,
                        canonical_field=best_target,
                        confidence=round(best_ratio, 3),
                        matching_method="fuzzy_match",
                        status="matched",
                        details=f"High-confidence fuzzy match ({best_ratio:.2f}) to canonical '{best_target}'",
                    )
                else:
                    # Borderline fuzzy match (0.85 - 0.92) requires manual confirmation
                    return ColumnMapping(
                        original_column=raw_column,
                        canonical_field=best_target,
                        confidence=round(best_ratio, 3),
                        matching_method="fuzzy_match",
                        status="uncertain",
                        details=f"Moderate fuzzy match ({best_ratio:.2f}) to '{best_target}'. Flagged for manual confirmation.",
                    )

        # Stage 5: Unmatched / Uncertain
        return ColumnMapping(
            original_column=raw_column,
            canonical_field=None,
            confidence=0.0,
            matching_method="unmatched",
            status="unmapped",
            details="No canonical alias or verified fuzzy match found",
        )

    def identify_mappings(
        self,
        columns: List[str],
        custom_mappings: Optional[Dict[str, str]] = None,
    ) -> Dict[str, ColumnMapping]:
        """
        Analyze all dataset columns and resolve mappings, detecting and reporting conflicts.
        Preserves custom overrides if provided.
        """
        custom_mappings = custom_mappings or {}
        mappings: Dict[str, ColumnMapping] = {}

        # 1. First pass: individual matching
        for col in columns:
            if col in custom_mappings:
                target = custom_mappings[col]
                if target in CANONICAL_FIELDS:
                    mappings[col] = ColumnMapping(
                        original_column=col,
                        canonical_field=target,
                        confidence=1.0,
                        matching_method="manual_override",
                        status="matched",
                        details=f"Explicitly mapped to '{target}' by user",
                    )
                else:
                    mappings[col] = ColumnMapping(
                        original_column=col,
                        canonical_field=None,
                        confidence=0.0,
                        matching_method="manual_override",
                        status="uncertain",
                        details=f"Provided target '{target}' is not a recognized canonical field",
                    )
            else:
                mappings[col] = self.identify_column(col)

        # 2. Second pass: conflict detection
        # Check if multiple source columns map to the same canonical target
        target_to_cols: Dict[str, List[str]] = {}
        for col, mapping in mappings.items():
            if mapping.canonical_field:
                target_to_cols.setdefault(mapping.canonical_field, []).append(col)

        for target, mapped_cols in target_to_cols.items():
            if len(mapped_cols) > 1:
                for col in mapped_cols:
                    mappings[col].status = "conflict"
                    mappings[col].details = (
                        f"Conflict: target '{target}' is claimed by multiple columns: {mapped_cols}"
                    )

        return mappings

    def create_normalization_report(
        self,
        columns: List[str],
        mappings: Dict[str, ColumnMapping],
        total_records: int = 0,
        valid_records: int = 0,
        duplicate_records: int = 0,
    ) -> NormalizationReport:
        """Build a comprehensive NormalizationReport summary."""
        mapped_count = sum(1 for m in mappings.values() if m.canonical_field is not None and m.status == "matched")
        unmapped_count = sum(1 for m in mappings.values() if m.status == "unmapped")
        uncertain_count = sum(1 for m in mappings.values() if m.status == "uncertain")

        # Group conflicts
        target_to_cols: Dict[str, List[str]] = {}
        for col, mapping in mappings.items():
            if mapping.canonical_field:
                target_to_cols.setdefault(mapping.canonical_field, []).append(col)

        conflicts: List[str] = []
        for target, cols in target_to_cols.items():
            if len(cols) > 1:
                conflicts.append(
                    f"{target}: multiple source columns {cols}. Primary value selected from '{cols[0]}'; all original column values preserved."
                )

        return NormalizationReport(
            total_columns=len(columns),
            mapped_columns=mapped_count,
            unmapped_columns=unmapped_count,
            uncertain_columns=uncertain_count,
            conflicts=conflicts,
            mappings=mappings,
            total_records=total_records,
            valid_records=valid_records,
            duplicate_records=duplicate_records,
        )

    # -----------------------------------------------------------------------
    # Value Parsers & Field Normalizers
    # -----------------------------------------------------------------------

    @staticmethod
    def _is_empty_or_na(val: Any) -> bool:
        """Check if a value represents empty or null."""
        if val is None:
            return True
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return True
        if isinstance(val, str):
            s = val.strip().lower()
            return s in ("", "nan", "none", "null", "n/a", "na", "<na>", "undefined")
        return False

    @classmethod
    def _clean_doi(cls, val: Any) -> Optional[str]:
        """Clean and validate DOI value. Returns None if invalid or absent."""
        if cls._is_empty_or_na(val):
            return None
        s = str(val).strip()
        match = re.search(r"(?:https?://(?:dx\.)?doi\.org/|doi:\s*)?(10\.\d{4,9}/[^\s]+)", s, re.IGNORECASE)
        if match:
            clean_doi = match.group(1).rstrip("/.,;)").strip()
            if len(clean_doi) > 6 and "/" in clean_doi:
                return clean_doi
        return None

    @classmethod
    def _clean_pmid(cls, val: Any) -> Optional[str]:
        """Clean and validate PMID value. Returns None if invalid or absent."""
        if cls._is_empty_or_na(val):
            return None
        s = str(val).strip()
        match = re.search(r"\b(\d{4,10})\b", s)
        if match:
            return match.group(1)
        return None

    @classmethod
    def _clean_url(cls, val: Any) -> Optional[str]:
        """Clean and validate URL string. Returns None if invalid or absent."""
        if cls._is_empty_or_na(val):
            return None
        s = str(val).strip()
        if re.match(r"^(https?|ftp)://[^\s]+", s, re.IGNORECASE):
            return s
        return None

    @classmethod
    def _parse_year(cls, val: Any) -> Optional[int]:
        """Conservatively parse and validate a 4-digit publication year (1800 - 2035)."""
        if cls._is_empty_or_na(val):
            return None
        # Direct numeric check
        if isinstance(val, (int, float)):
            try:
                if math.isnan(val) or math.isinf(val):
                    return None
                if math.isclose(val, round(val), abs_tol=1e-3):
                    y = int(round(val))
                    if 1800 <= y <= 2035:
                        return y
            except (ValueError, OverflowError):
                pass
        # String extraction (find 4-digit year pattern)
        s = str(val).strip()
        match = re.search(r"\b(18\d{2}|19\d{2}|20\d{2})\b", s)
        if match:
            y = int(match.group(1))
            if 1800 <= y <= 2035:
                return y
        return None

    @classmethod
    def _parse_citation_count(cls, val: Any) -> Optional[int]:
        """Safely parse non-negative integer citation count."""
        if cls._is_empty_or_na(val):
            return None
        try:
            val_float = float(val)
            if math.isnan(val_float) or math.isinf(val_float):
                return None
            cnt = int(val_float)
            return cnt if cnt >= 0 else None
        except (ValueError, TypeError, OverflowError):
            return None

    @classmethod
    def _parse_boolean(cls, val: Any) -> Optional[bool]:
        """Parse boolean flag from various representations."""
        if cls._is_empty_or_na(val):
            return None
        if isinstance(val, bool):
            return val
        s = str(val).strip().lower()
        if s in ("true", "1", "yes", "t", "y", "open", "oa"):
            return True
        if s in ("false", "0", "no", "f", "n", "closed"):
            return False
        return None

    @classmethod
    def _parse_list_field(
        cls,
        val: Any,
        is_author: bool = False,
        is_affiliation: bool = False,
    ) -> List[str]:
        """
        Parse multi-value metadata strings into a clean list of strings.
        Handles lists, JSON arrays, semicolons, pipes, and commas.
        For affiliations, commas are preserved within individual address strings.
        """
        if cls._is_empty_or_na(val):
            return []

        # If already a list or tuple
        if isinstance(val, (list, tuple, set)):
            res: List[str] = []
            for item in val:
                s = str(item).strip()
                if s and s not in res:
                    res.append(s)
            return res

        s = str(val).strip()
        if not s:
            return []

        # Check for JSON-style or Python list string: ["a", "b"]
        if (s.startswith("[") and s.endswith("]")) or (s.startswith("(") and s.endswith(")")):
            try:
                parsed = json.loads(s.replace("'", '"'))
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if str(x).strip()]
            except Exception:
                try:
                    parsed = ast.literal_eval(s)
                    if isinstance(parsed, (list, tuple)):
                        return [str(x).strip() for x in parsed if str(x).strip()]
                except Exception:
                    pass
            # Strip outer brackets if parsing failed
            s = s.strip("[]()")

        # Split priority: Semicolon > Pipe > Comma (careful with authors and affiliations)
        if ";" in s:
            raw_items = s.split(";")
        elif "|" in s:
            raw_items = s.split("|")
        elif is_affiliation:
            # Affiliations contain commas internally (e.g. "Google Brain, Mountain View, CA, USA")
            # Do NOT split by comma unless separated by semicolons or pipes
            raw_items = [s]
        elif not is_author and "," in s:
            raw_items = s.split(",")
        elif is_author and "," in s:
            # If authors are comma-separated, check if it's "Last, First" or "Author1, Author2"
            # Single comma likely means "Last, First" -> keep as single author
            comma_count = s.count(",")
            if comma_count == 1:
                raw_items = [s]
            else:
                raw_items = s.split(",")
        else:
            raw_items = [s]

        # Clean and deduplicate while preserving order
        deduped: List[str] = []
        for item in raw_items:
            cleaned = item.strip().strip("'\"`")
            if cleaned and cleaned not in deduped:
                deduped.append(cleaned)
        return deduped

    @classmethod
    def _resolve_paper_id(
        cls,
        doi: Optional[str],
        pmid: Optional[str],
        openalex_id: Optional[str],
        pmcid: Optional[str],
        raw_paper_id: Optional[str],
        record_id: str,
    ) -> str:
        """
        Derive the academic paper identifier without inventing fake DOIs or PMIDs.
        Uses explicit identifiers first; falls back cleanly to the record identifier.
        """
        if doi and doi.strip():
            return doi.strip().lower()
        if pmid and pmid.strip():
            return f"pmid_{pmid.strip()}"
        if openalex_id and openalex_id.strip():
            return openalex_id.strip()
        if pmcid and pmcid.strip():
            return pmcid.strip().lower()
        if raw_paper_id and raw_paper_id.strip():
            return raw_paper_id.strip()
        return record_id

    # -----------------------------------------------------------------------
    # Record Transformation
    # -----------------------------------------------------------------------

    def normalize_row_to_record(
        self,
        row_dict: Dict[str, Any],
        mappings: Dict[str, ColumnMapping],
        row_index: int,
    ) -> CanonicalPaperRecord:
        """
        Transform a single raw data dictionary into a CanonicalPaperRecord.
        Preserves original unmapped and mapped columns in raw_data, and
        records any scalar conflict discrepancies in conflicting_values.
        """
        record_id = f"record_{row_index + 1}"

        # Bucket original columns by their canonical targets
        canonical_values: Dict[str, List[Tuple[str, Any]]] = {}
        for col_name, val in row_dict.items():
            mapping = mappings.get(col_name)
            if mapping and mapping.canonical_field:
                canonical_values.setdefault(mapping.canonical_field, []).append((col_name, val))

        # Track conflicting values across columns mapping to the same field
        conflicting_values: Dict[str, Dict[str, Any]] = {}
        for target, cols_and_vals in canonical_values.items():
            if len(cols_and_vals) > 1:
                non_empty = {col: val for col, val in cols_and_vals if not self._is_empty_or_na(val)}
                if len(non_empty) > 1:
                    conflicting_values[target] = non_empty

        def get_scalar(field_name: str) -> Optional[Any]:
            """Retrieve the best non-empty value for a scalar canonical field."""
            candidates = canonical_values.get(field_name, [])
            for _, val in candidates:
                if not self._is_empty_or_na(val):
                    return val
            return None

        def get_merged_list(
            field_name: str,
            is_author: bool = False,
            is_affiliation: bool = False,
        ) -> List[str]:
            """Merge items from all conflicting/multiple columns mapping to this field."""
            candidates = canonical_values.get(field_name, [])
            merged: List[str] = []
            for _, val in candidates:
                items = self._parse_list_field(val, is_author=is_author, is_affiliation=is_affiliation)
                for item in items:
                    if item not in merged:
                        merged.append(item)
            return merged

        # Extract & parse individual canonical attributes
        raw_title = get_scalar("title")
        title = str(raw_title).strip() if raw_title and not self._is_empty_or_na(raw_title) else "Unknown Title"

        raw_abstract = get_scalar("abstract")
        abstract = str(raw_abstract).strip() if raw_abstract and not self._is_empty_or_na(raw_abstract) else None

        authors = get_merged_list("authors", is_author=True)
        affiliations = get_merged_list("affiliations", is_affiliation=True)
        countries = get_merged_list("countries", is_author=False)
        keywords = get_merged_list("keywords", is_author=False)

        publication_year = self._parse_year(get_scalar("publication_year"))

        raw_pub_date = get_scalar("publication_date")
        publication_date = str(raw_pub_date).strip() if raw_pub_date and not self._is_empty_or_na(raw_pub_date) else None

        raw_journal = get_scalar("journal")
        journal = str(raw_journal).strip() if raw_journal and not self._is_empty_or_na(raw_journal) else None

        doi = self._clean_doi(get_scalar("doi"))
        pmid = self._clean_pmid(get_scalar("pmid"))

        raw_pmcid = get_scalar("pmcid")
        pmcid = str(raw_pmcid).strip() if raw_pmcid and not self._is_empty_or_na(raw_pmcid) else None

        raw_openalex_id = get_scalar("openalex_id")
        openalex_id = str(raw_openalex_id).strip() if raw_openalex_id and not self._is_empty_or_na(raw_openalex_id) else None

        citation_count = self._parse_citation_count(get_scalar("citation_count"))

        raw_pub_type = get_scalar("publication_type")
        publication_type = str(raw_pub_type).strip() if raw_pub_type and not self._is_empty_or_na(raw_pub_type) else None

        url = self._clean_url(get_scalar("url"))
        download_url = self._clean_url(get_scalar("download_url"))

        is_open_access = self._parse_boolean(get_scalar("is_open_access"))

        raw_paper_id = get_scalar("paper_id")
        paper_id_str = str(raw_paper_id).strip() if raw_paper_id and not self._is_empty_or_na(raw_paper_id) else None
        paper_id = self._resolve_paper_id(doi, pmid, openalex_id, pmcid, paper_id_str, record_id)

        # Preserve the entire original row intact in raw_data
        raw_data = dict(row_dict)

        return CanonicalPaperRecord(
            record_id=record_id,
            paper_id=paper_id,
            title=title,
            abstract=abstract,
            authors=authors,
            affiliations=affiliations,
            countries=countries,
            keywords=keywords,
            publication_year=publication_year,
            publication_date=publication_date,
            journal=journal,
            doi=doi,
            pmid=pmid,
            pmcid=pmcid,
            openalex_id=openalex_id,
            citation_count=citation_count,
            publication_type=publication_type,
            url=url,
            download_url=download_url,
            is_open_access=is_open_access,
            raw_data=raw_data,
            conflicting_values=conflicting_values,
        )

    def normalize_dataframe(
        self,
        df: pd.DataFrame,
        custom_mappings: Optional[Dict[str, str]] = None,
    ) -> Tuple[List[CanonicalPaperRecord], NormalizationReport]:
        """
        Normalize a pandas DataFrame into CanonicalPaperRecords.
        Does NOT modify the input DataFrame.
        Tracks duplicate papers based on paper_id.
        """
        if df.empty:
            cols = list(df.columns)
            mappings = self.identify_mappings(cols, custom_mappings)
            report = self.create_normalization_report(cols, mappings, total_records=0, valid_records=0, duplicate_records=0)
            return [], report

        cols = list(df.columns)
        mappings = self.identify_mappings(cols, custom_mappings)

        records: List[CanonicalPaperRecord] = []
        seen_paper_ids: Dict[str, str] = {}
        duplicate_count = 0

        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            record = self.normalize_row_to_record(row_dict, mappings, int(idx))

            # Distinguish unique records from duplicate research papers
            if record.paper_id in seen_paper_ids:
                record.is_duplicate = True
                record.duplicate_of = seen_paper_ids[record.paper_id]
                duplicate_count += 1
            else:
                record.is_duplicate = False
                record.duplicate_of = None
                seen_paper_ids[record.paper_id] = record.record_id

            records.append(record)

        report = self.create_normalization_report(
            cols,
            mappings,
            total_records=len(df),
            valid_records=len(records),
            duplicate_records=duplicate_count,
        )
        return records, report

    def normalize_records(
        self,
        records: List[Dict[str, Any]],
        custom_mappings: Optional[Dict[str, str]] = None,
    ) -> Tuple[List[CanonicalPaperRecord], NormalizationReport]:
        """
        Normalize a list of raw row dictionaries into CanonicalPaperRecords.
        Does NOT modify the input dictionaries.
        """
        if not records:
            report = self.create_normalization_report([], {}, total_records=0, valid_records=0, duplicate_records=0)
            return [], report

        # Collect union of all column keys across records
        cols_set: Set[str] = set()
        for r in records:
            cols_set.update(r.keys())
        cols = list(cols_set)

        mappings = self.identify_mappings(cols, custom_mappings)

        normalized_records: List[CanonicalPaperRecord] = []
        seen_paper_ids: Dict[str, str] = {}
        duplicate_count = 0

        for idx, r in enumerate(records):
            record = self.normalize_row_to_record(r, mappings, idx)

            if record.paper_id in seen_paper_ids:
                record.is_duplicate = True
                record.duplicate_of = seen_paper_ids[record.paper_id]
                duplicate_count += 1
            else:
                record.is_duplicate = False
                record.duplicate_of = None
                seen_paper_ids[record.paper_id] = record.record_id

            normalized_records.append(record)

        report = self.create_normalization_report(
            cols,
            mappings,
            total_records=len(records),
            valid_records=len(normalized_records),
            duplicate_records=duplicate_count,
        )
        return normalized_records, report
