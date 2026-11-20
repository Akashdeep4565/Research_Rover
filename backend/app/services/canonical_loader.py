"""
Shared Canonical Dataset Loader and Cache Manager for Research Rover.

Bridges raw CSV datasets to standardized CanonicalPaperRecords, managing
metadata sidecars (*_canonical_metadata.json), providing unified DataFrames
with both canonical and legacy column aliases, and evaluating runtime
index availability for downstream services.
"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from app.utils.csv_loader import read_csv_to_dataframe, CSVLoadError
from app.services.dataset_normalizer import (
    CanonicalPaperRecord,
    ColumnMapping,
    DatasetNormalizer,
    NormalizationReport,
)
from app.services.dataset_quality import (
    DatasetQualityAssessor,
    DatasetQualityReport,
    FeatureReadiness,
    FeatureReadinessStatus,
)

logger = logging.getLogger("research_rover")


class CanonicalDataLoader:
    """
    Centralized canonical loader and sidecar manager.
    Used by analysis_service, country_service, search_service, and embedding_service.
    """

    @staticmethod
    def resolve_csv_path(filename_or_path: str, data_folder: Optional[str] = None) -> str:
        """Resolve a filename or absolute path to a safe, verified CSV file path."""
        if os.path.isabs(filename_or_path) and os.path.exists(filename_or_path):
            return filename_or_path

        base_name = os.path.basename(filename_or_path)
        if not data_folder:
            # Default fallback relative to project structure
            data_folder = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
            )

        resolved = os.path.join(data_folder, base_name)
        return resolved

    @staticmethod
    def get_metadata_sidecar_path(csv_path: str) -> str:
        """Get the file path for the canonical metadata sidecar JSON."""
        dir_name = os.path.dirname(os.path.abspath(csv_path))
        base_name = os.path.splitext(os.path.basename(csv_path))[0]
        return os.path.join(dir_name, f"{base_name}_canonical_metadata.json")

    @classmethod
    def check_index_files_exist(cls, csv_path: str, data_folder: Optional[str] = None) -> Tuple[bool, str]:
        """
        Check if FAISS index and metadata files exist for the dataset.
        Returns (exists: bool, status_str: 'indexed' | 'not_indexed').
        """
        dir_name = data_folder or os.path.dirname(os.path.abspath(csv_path))
        base_name = os.path.splitext(os.path.basename(csv_path))[0]

        index_file = os.path.join(dir_name, f"{base_name}_paper_chunks_hdbscan.index")
        metadata_file = os.path.join(dir_name, f"{base_name}_paper_chunk_metadata_hdbscan.json")

        if os.path.exists(index_file) and os.path.exists(metadata_file):
            return True, "indexed"
        return False, "not_indexed"

    @classmethod
    def process_and_save_canonical(
        cls,
        csv_path: str,
        custom_mappings: Optional[Dict[str, str]] = None,
    ) -> Tuple[List[CanonicalPaperRecord], DatasetQualityReport]:
        """
        Load CSV, normalize with DatasetNormalizer, assess with DatasetQualityAssessor,
        save canonical sidecar JSON, and return the records and report.
        Preserves original CSV untouched.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        df = read_csv_to_dataframe(csv_path)

        normalizer = DatasetNormalizer()
        records, norm_report = normalizer.normalize_dataframe(df, custom_mappings=custom_mappings)

        assessor = DatasetQualityAssessor()
        quality_report = assessor.assess(records, normalization_report=norm_report)

        # Write canonical metadata sidecar
        sidecar_path = cls.get_metadata_sidecar_path(csv_path)
        try:
            sidecar_payload = {
                "filename": os.path.basename(csv_path),
                "total_records": len(records),
                "valid_records": quality_report.valid_records,
                "duplicate_records": quality_report.duplicate_records,
                "overall_quality_score": quality_report.overall_quality_score,
                "quality_grade": quality_report.quality_grade,
                "canonical_fields_detected": [
                    m.canonical_field for m in norm_report.mappings.values() if m.canonical_field
                ],
                "column_mappings": {
                    col: m.model_dump() if hasattr(m, "model_dump") else m.dict()
                    for col, m in norm_report.mappings.items()
                },
                "unmapped_columns": quality_report.unmapped_columns,
                "conflicts": norm_report.conflicts,
                "feature_readiness": {
                    fid: fr.model_dump() if hasattr(fr, "model_dump") else fr.dict()
                    for fid, fr in quality_report.feature_readiness.items()
                },
                "recommendations": quality_report.recommendations,
                "generated_at": time.time(),
                "csv_mtime": os.path.getmtime(csv_path),
            }

            with open(sidecar_path, "w", encoding="utf-8") as f:
                json.dump(sidecar_payload, f, indent=2, ensure_ascii=False)

            logger.info("Saved canonical metadata sidecar: %s", sidecar_path)
        except Exception as e:
            logger.warning("Could not save canonical sidecar for %s: %s", csv_path, e)

        return records, quality_report

    @classmethod
    def apply_index_status_overlay(
        cls,
        quality_report: DatasetQualityReport,
        index_exists: bool,
    ) -> DatasetQualityReport:
        """
        Overlay runtime FAISS vector index status onto feature readiness.
        If index is missing, semantic_search and ai_chat_rag are downgraded
        from READY to PARTIALLY_READY with explicit actionable warnings.
        Shared across upload and quality endpoints for 100% consistency.
        """
        if not index_exists:
            # Semantic search overlay
            if "semantic_search" in quality_report.feature_readiness:
                sr = quality_report.feature_readiness["semantic_search"]
                if sr.status == FeatureReadinessStatus.READY:
                    sr.status = FeatureReadinessStatus.PARTIALLY_READY
                msg = (
                    "Vector index (*_paper_chunks_hdbscan.index) has not been built yet. "
                    "Generate embeddings to enable vector retrieval."
                )
                if msg not in sr.warnings:
                    sr.warnings.append(msg)

            # AI chat RAG overlay
            if "ai_chat_rag" in quality_report.feature_readiness:
                cr = quality_report.feature_readiness["ai_chat_rag"]
                if cr.status == FeatureReadinessStatus.READY:
                    cr.status = FeatureReadinessStatus.PARTIALLY_READY
                msg = (
                    "AI search index not found on disk. "
                    "Chat will operate in general mode without paper context until embeddings are built."
                )
                if msg not in cr.warnings:
                    cr.warnings.append(msg)

        return quality_report

    @classmethod
    def load_canonical_records(
        cls,
        csv_path_or_filename: str,
        exclude_duplicates: bool = False,
    ) -> List[CanonicalPaperRecord]:
        """
        Load normalized CanonicalPaperRecords for a CSV file.
        Uses cached sidecar if up-to-date, or computes on-the-fly.
        If exclude_duplicates is True, filters out records flagged as duplicates.
        """
        csv_path = cls.resolve_csv_path(csv_path_or_filename)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path_or_filename}")

        # Check if sidecar exists and is newer than CSV
        sidecar_path = cls.get_metadata_sidecar_path(csv_path)
        csv_mtime = os.path.getmtime(csv_path)

        if not os.path.exists(sidecar_path) or os.path.getmtime(sidecar_path) < csv_mtime:
            # Recompute and update sidecar
            records, _ = cls.process_and_save_canonical(csv_path)
        else:
            # Sidecar exists; normalize dataframe to obtain full strongly-typed CanonicalPaperRecords
            df = read_csv_to_dataframe(csv_path)
            normalizer = DatasetNormalizer()
            records, _ = normalizer.normalize_dataframe(df)

        if exclude_duplicates:
            records = [r for r in records if not r.is_duplicate]

        return records

    @classmethod
    def load_canonical_dataframe(
        cls,
        csv_path_or_filename: str,
        exclude_duplicates: bool = False,
    ) -> pd.DataFrame:
        """
        Load a normalized pandas DataFrame.
        Contains:
        1. Canonical lowercase columns (title, abstract, authors, affiliations, keywords, publication_year, doi, journal, download_url)
        2. Legacy capitalized alias columns (Title, Abstract, Authors, Affiliations, Keywords, Publication Year, Year_Published, DOI, Source)
        3. All raw unmapped original columns.
        If exclude_duplicates is True, filters out duplicate records.
        Guarantees 100% backward compatibility for legacy pandas queries.
        """
        records = cls.load_canonical_records(csv_path_or_filename, exclude_duplicates=exclude_duplicates)
        if not records:
            return pd.DataFrame()

        rows: List[Dict[str, Any]] = []
        for r in records:
            # Seed with raw data so original custom columns are preserved
            row_dict = dict(r.raw_data)

            # Add canonical lowercase fields
            row_dict["paper_id"] = r.paper_id
            row_dict["title"] = r.title
            row_dict["abstract"] = r.abstract or ""
            row_dict["authors"] = r.authors
            row_dict["affiliations"] = r.affiliations
            row_dict["countries"] = r.countries
            row_dict["keywords"] = r.keywords
            row_dict["publication_year"] = r.publication_year
            row_dict["publication_date"] = r.publication_date or ""
            row_dict["journal"] = r.journal or ""
            row_dict["doi"] = r.doi or ""
            row_dict["pmid"] = r.pmid or ""
            row_dict["pmcid"] = r.pmcid or ""
            row_dict["openalex_id"] = r.openalex_id or ""
            row_dict["citation_count"] = r.citation_count
            row_dict["download_url"] = r.download_url or ""
            row_dict["url"] = r.url or ""
            row_dict["is_open_access"] = r.is_open_access
            row_dict["is_duplicate"] = r.is_duplicate
            row_dict["duplicate_of"] = r.duplicate_of

            # Add legacy capitalized aliases for backward compatibility
            row_dict["Title"] = r.title
            row_dict["Abstract"] = r.abstract or ""
            row_dict["Authors"] = "; ".join(r.authors) if r.authors else ""
            row_dict["Affiliations"] = "; ".join(r.affiliations) if r.affiliations else ""
            row_dict["Keywords"] = "; ".join(r.keywords) if r.keywords else ""
            row_dict["Publication Year"] = r.publication_year if r.publication_year else ""
            row_dict["Year_Published"] = r.publication_year if r.publication_year else 0
            row_dict["DOI"] = r.doi or ""
            row_dict["Doi"] = r.doi or ""
            row_dict["Source"] = r.journal or "Unknown"
            row_dict["Journal/Book"] = r.journal or "Unknown"
            row_dict["Download_URL"] = r.download_url or ""

            rows.append(row_dict)

        return pd.DataFrame(rows)

    @classmethod
    def get_quality_report(
        cls,
        csv_path_or_filename: str,
        data_folder: Optional[str] = None,
    ) -> DatasetQualityReport:
        """
        Get or compute the DatasetQualityReport for a CSV file.
        Overlays runtime index availability onto feature readiness via shared apply_index_status_overlay.
        """
        csv_path = cls.resolve_csv_path(csv_path_or_filename, data_folder=data_folder)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path_or_filename}")

        sidecar_path = cls.get_metadata_sidecar_path(csv_path)
        csv_mtime = os.path.getmtime(csv_path)

        if not os.path.exists(sidecar_path) or os.path.getmtime(sidecar_path) < csv_mtime:
            _, quality_report = cls.process_and_save_canonical(csv_path)
        else:
            # Reconstruct from normalizer/assessor
            records = cls.load_canonical_records(csv_path)
            assessor = DatasetQualityAssessor()
            normalizer = DatasetNormalizer()
            df = read_csv_to_dataframe(csv_path)
            _, norm_report = normalizer.normalize_dataframe(df)
            quality_report = assessor.assess(records, normalization_report=norm_report)

        # Distinguish data readiness from runtime index status using shared overlay
        index_exists, _ = cls.check_index_files_exist(csv_path, data_folder=data_folder)
        return cls.apply_index_status_overlay(quality_report, index_exists)
