"""
PubMed Affiliation Enricher Service for Research Rover.

Enriches existing Research Rover topic-search CSV files by fetching author affiliations
from PubMed XML via batch EFetch requests and populating the 'Affiliations' column.
"""

import argparse
import logging
import os
import shutil
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from xml.etree import ElementTree as ET

from app.core.config import get_settings
from app.services.country_service import CountryService
from app.services.pubmed_service import PubMedService
from app.utils.csv_loader import read_csv_to_dataframe, read_csv_to_records, detect_csv_encoding

logger = logging.getLogger("research_rover")


class PubMedAffiliationEnricher:
    """Service to enrich Research Rover CSV datasets with PubMed affiliation metadata."""

    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None):
        settings = get_settings()
        self.email = email or settings.EMAIL or "user@example.com"
        self.api_key = api_key or settings.PUBMED_API_KEY
        self.pubmed_service = PubMedService(email=self.email, api_key=self.api_key)

    @staticmethod
    def resolve_csv_path(path_or_filename: str) -> str:
        """Resolve full CSV path, checking data directory if needed."""
        if os.path.exists(path_or_filename):
            return os.path.abspath(path_or_filename)

        settings = get_settings()
        basename = os.path.basename(path_or_filename)
        data_path = os.path.join(settings.DATA_FOLDER, basename)
        if os.path.exists(data_path):
            return os.path.abspath(data_path)

        raise FileNotFoundError(f"CSV file not found: {path_or_filename}")

    @staticmethod
    def detect_pmid_column(df: pd.DataFrame) -> Optional[str]:
        """Identify the column name containing PMIDs in the DataFrame."""
        for col in ("PMID", "pmid", "Pmid", "Id", "id"):
            if col in df.columns:
                return col
        return None

    def fetch_affiliations_batch(
        self, pmids: List[str], batch_size: int = 50
    ) -> Dict[str, List[str]]:
        """
        Fetch author affiliations from PubMed XML in batches of 50 PMIDs.
        Returns a mapping of PMID -> list of extracted affiliation strings.
        """
        pmid_affiliation_map: Dict[str, List[str]] = {}
        valid_pmids = [p for p in pmids if p and str(p).strip().isdigit()]

        for i in range(0, len(valid_pmids), batch_size):
            batch = valid_pmids[i : i + batch_size]
            try:
                efetch_data = {
                    "db": "pubmed",
                    "id": ",".join(batch),
                    "retmode": "xml",
                }
                response = self.pubmed_service._post_with_retry("efetch.fcgi", efetch_data)
                root = ET.fromstring(response.content)

                for article in root.findall(".//PubmedArticle"):
                    pmid_elem = article.find(".//PMID")
                    if pmid_elem is not None and pmid_elem.text:
                        pmid_str = pmid_elem.text.strip()
                        affs = []
                        for aff_elem in article.findall(".//AffiliationInfo/Affiliation"):
                            if aff_elem is not None:
                                text = "".join(aff_elem.itertext()).strip()
                                if text and text not in affs:
                                    affs.append(text)
                        pmid_affiliation_map[pmid_str] = affs
            except Exception as e:
                logger.error(f"Error fetching affiliations for batch {i//batch_size + 1}: {e}")
                continue

        return pmid_affiliation_map

    def enrich_csv(
        self,
        csv_path_input: str,
        force: bool = False,
        batch_size: int = 50,
        progress_callback: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Enrich a CSV file with affiliations retrieved from PubMed.
        Performs atomic safe saving and invalidates CountryService cache.
        """
        csv_path = self.resolve_csv_path(csv_path_input)
        df = read_csv_to_dataframe(csv_path)

        total_papers = len(df)
        pmid_col = self.detect_pmid_column(df)
        if not pmid_col:
            raise ValueError(f"No PMID column found in CSV: {csv_path}")

        if "Affiliations" not in df.columns:
            df["Affiliations"] = ""

        def is_empty_aff(val):
            if val is None or pd.isna(val):
                return True
            s = str(val).strip()
            return not s or s.lower() in {"nan", "none", "null", "[]", "{}"}

        # Identify rows needing enrichment
        rows_to_enrich_indices = []
        already_valid_count = 0

        for idx, row in df.iterrows():
            aff_val = row.get("Affiliations")
            pmid_val = str(row.get(pmid_col, "")).strip()

            if pmid_val and pmid_val.isdigit():
                if force or is_empty_aff(aff_val):
                    rows_to_enrich_indices.append(idx)
                else:
                    already_valid_count += 1

        pmids_to_fetch = [
            str(df.at[idx, pmid_col]).strip() for idx in rows_to_enrich_indices
        ]
        needed_count = len(pmids_to_fetch)

        if progress_callback:
            progress_callback("start", {
                "total_papers": total_papers,
                "already_valid_count": already_valid_count,
                "needed_count": needed_count,
                "batch_size": batch_size,
            })

        recovered_count = 0
        still_unavailable_count = 0

        if needed_count > 0:
            total_batches = (needed_count + batch_size - 1) // batch_size
            pmid_to_affs_map = {}

            for b_idx in range(total_batches):
                start_i = b_idx * batch_size
                batch_pmids = pmids_to_fetch[start_i : start_i + batch_size]

                if progress_callback:
                    progress_callback("batch", {
                        "batch_num": b_idx + 1,
                        "total_batches": total_batches,
                        "pmids_count": len(batch_pmids),
                    })

                batch_res = self.fetch_affiliations_batch(batch_pmids, batch_size=batch_size)
                pmid_to_affs_map.update(batch_res)

            # Update DataFrame with recovered affiliations
            for idx in rows_to_enrich_indices:
                pmid_val = str(df.at[idx, pmid_col]).strip()
                affs = pmid_to_affs_map.get(pmid_val, [])
                if affs:
                    aff_str = "; ".join([str(a).strip() for a in affs if str(a).strip()])
                    df.at[idx, "Affiliations"] = aff_str
                    recovered_count += 1
                else:
                    still_unavailable_count += 1

        # Save backup before writing
        backup_path = csv_path + ".backup"
        shutil.copy2(csv_path, backup_path)
        logger.info(f"Created backup file: {backup_path}")

        # Atomic save strategy: write to temporary file, then replace
        temp_path = csv_path + ".tmp"
        df.to_csv(temp_path, index=False, encoding="utf-8-sig")
        os.replace(temp_path, csv_path)
        logger.info(f"Successfully enriched and saved CSV to {csv_path}")

        # Invalidate CountryService in-memory cache for this file
        try:
            cs = CountryService()
            abs_path = os.path.abspath(csv_path)
            stale = [k for k in cs._CACHE if k[0] == abs_path]
            for k in stale:
                del cs._CACHE[k]
        except Exception as e:
            logger.warning(f"Unable to invalidate CountryService cache: {e}")

        summary = {
            "csv_path": csv_path,
            "backup_path": backup_path,
            "total_papers": total_papers,
            "already_valid_before": already_valid_count,
            "requested_from_pubmed": needed_count,
            "affiliations_recovered": recovered_count,
            "still_unavailable": still_unavailable_count,
            "total_papers_with_affiliations_after": already_valid_count + recovered_count,
        }

        if progress_callback:
            progress_callback("done", summary)

        return summary


def main():
    """CLI entry point for running PubMed affiliation enrichment."""
    parser = argparse.ArgumentParser(
        description="Enrich Research Rover CSV dataset with PubMed affiliation metadata."
    )
    parser.add_argument(
        "csv_file", help="Path or filename of the Research Rover CSV dataset to enrich."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download affiliations from PubMed even for papers that already have them.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size for PubMed EFetch requests (default: 50).",
    )

    args = parser.parse_args()

    def print_progress(stage, data):
        if stage == "start":
            print("==================================================================")
            print("RESEARCH ROVER — PUBMED AFFILIATION ENRICHER")
            print("==================================================================")
            print("Loading CSV...")
            print(f"Total papers: {data['total_papers']}")
            print(f"Papers already containing affiliations: {data['already_valid_count']}")
            print(f"Papers requiring enrichment: {data['needed_count']}\n")
            if data['needed_count'] > 0:
                print("Fetching PubMed affiliations...")
        elif stage == "batch":
            print(f"Batch {data['batch_num']}/{data['total_batches']} ({data['pmids_count']} PMIDs)")
        elif stage == "done":
            print("\n------------------------------------------------------------------")
            print(f"Affiliations recovered: {data['affiliations_recovered']}")
            print(f"Still unavailable: {data['still_unavailable']}")
            print("Saving enriched CSV...")
            print(f"Backup created: {data['backup_path']}")
            print(f"Enriched dataset saved: {data['csv_path']}")
            print("Done.")
            print("==================================================================")

    try:
        enricher = PubMedAffiliationEnricher()
        enricher.enrich_csv(
            csv_path_input=args.csv_file,
            force=args.force,
            batch_size=args.batch_size,
            progress_callback=print_progress,
        )
    except Exception as e:
        print(f"\n[ERROR] Enrichment failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
