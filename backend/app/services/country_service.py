"""
Country analysis service for Research Rover.

Processes paper metadata and CSV files using the centralized CSV loader
to produce country frequency distributions and international collaboration co-authorship networks.
"""

from collections import Counter
from itertools import combinations
import logging
from typing import Any, Dict, List, Optional, Tuple

from app.utils.country_extractor import extract_countries_from_affiliations, get_country_iso3

# Centralized CSV loader import with fallback for test runner environments
try:
    from app.utils.csv_loader import read_csv_to_records
except ImportError:
    from utils.csv_loader import read_csv_to_records

logger = logging.getLogger("research_rover")


import os

class CountryService:
    """Service for bibliometric country extraction and international collaboration network generation."""

    # In-memory dataset cache keyed by (abs_path, mtime, size)
    _CACHE: Dict[Tuple[str, float, int], Dict[str, Any]] = {}

    @staticmethod
    def extract_countries_for_paper(paper_data: Dict[str, Any]) -> List[str]:
        """
        Extract deduplicated canonical country names for a single paper dictionary.
        Checks explicit affiliation fields first, accumulating across all present affiliation entries.
        Falls back to inspecting author fields if no explicit affiliation keys yielded countries.
        """
        if not paper_data or not isinstance(paper_data, dict):
            return []

        extracted_set: Set[str] = set()

        # Check if pre-extracted or canonical countries are present
        raw_countries = paper_data.get("countries") or paper_data.get("Countries")
        if raw_countries:
            if isinstance(raw_countries, list):
                for c in raw_countries:
                    if str(c).strip():
                        extracted_set.add(str(c).strip())
            elif isinstance(raw_countries, str) and raw_countries.strip():
                for c in extract_countries_from_affiliations(raw_countries):
                    extracted_set.add(c)

        # Check explicit affiliation keys
        for key in ("Affiliations", "affiliations", "Affiliation", "affiliation", "Address", "address"):
            val = paper_data.get(key)
            if val:
                countries = extract_countries_from_affiliations(val)
                for c in countries:
                    extracted_set.add(c)

        # Fallback to author fields if no countries were found in explicit affiliation keys
        if not extracted_set:
            authors = paper_data.get("Authors") or paper_data.get("authors")
            if authors:
                countries = extract_countries_from_affiliations(authors)
                for c in countries:
                    extracted_set.add(c)

        return sorted(list(extracted_set))

    def _get_or_compute_analysis(self, csv_path: str, exclude_duplicates: bool = True) -> Dict[str, Any]:
        """
        Internal helper to load a CSV, extract country affiliations, and build both frequency
        and collaboration structures in a single pass with mtime/size cache invalidation.
        Consumes canonical records via CanonicalDataLoader with safe fallback to raw CSV records.
        """
        abs_path = os.path.abspath(csv_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        mtime = os.path.getmtime(abs_path)
        size = os.path.getsize(abs_path)
        cache_key = (abs_path, mtime, size, exclude_duplicates)

        if cache_key in self._CACHE:
            return self._CACHE[cache_key]

        records: List[Dict[str, Any]] = []
        try:
            from app.services.canonical_loader import CanonicalDataLoader
            canonical_records = CanonicalDataLoader.load_canonical_records(
                csv_path, exclude_duplicates=exclude_duplicates
            )
            for r in canonical_records:
                rec_dict = dict(r.raw_data)
                rec_dict["countries"] = r.countries
                rec_dict["Countries"] = r.countries
                rec_dict["affiliations"] = "; ".join(r.affiliations) if r.affiliations else ""
                rec_dict["Affiliations"] = "; ".join(r.affiliations) if r.affiliations else ""
                rec_dict["title"] = r.title
                rec_dict["Title"] = r.title
                rec_dict["authors"] = "; ".join(r.authors) if r.authors else ""
                rec_dict["Authors"] = "; ".join(r.authors) if r.authors else ""
                rec_dict["year"] = str(r.publication_year) if r.publication_year else ""
                rec_dict["Publication Year"] = str(r.publication_year) if r.publication_year else ""
                rec_dict["Source"] = r.journal or "Unknown"
                rec_dict["paper_id"] = r.paper_id
                rec_dict["is_duplicate"] = r.is_duplicate
                records.append(rec_dict)
        except Exception as e:
            logger.warning("Canonical loader fallback in CountryService: %s", e)
            records = read_csv_to_records(csv_path)

        return self._compute_metrics_from_records(
            records,
            filename=os.path.basename(csv_path),
            cache_key=cache_key,
            abs_path=abs_path,
        )

    def _compute_metrics_from_records(
        self,
        records: List[Dict[str, Any]],
        filename: str = "",
        cache_key: Optional[Tuple[str, float, int]] = None,
        abs_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        total_papers = len(records)
        papers_with_country = 0
        international_papers = 0
        country_paper_counts: Counter[str] = Counter()
        collaboration_counts: Counter[Tuple[str, str]] = Counter()
        unassigned_papers: List[Dict[str, Any]] = []

        for idx, record in enumerate(records):
            extracted = self.extract_countries_for_paper(record)
            unique_countries = sorted(list(set(extracted))) if extracted else []

            if unique_countries:
                papers_with_country += 1
                if len(unique_countries) >= 2:
                    international_papers += 1
                for country in unique_countries:
                    country_paper_counts[country] += 1
                for source, target in combinations(unique_countries, 2):
                    collaboration_counts[(source, target)] += 1
            else:
                paper_id = (
                    record.get("PMID") or record.get("DOI") or record.get("Doi") or record.get("Title") or f"paper_{idx + 1}"
                )
                unassigned_papers.append({
                    "paper_id": str(paper_id),
                    "title": str(record.get("Title") or "Unknown Title").strip(),
                    "authors": record.get("Authors") or "",
                    "source": str(record.get("Source") or record.get("Journal/Book") or "Unknown").strip(),
                    "year": str(record.get("Publication Year") or record.get("Year_Published") or "").strip(),
                })

        papers_without_country = total_papers - papers_with_country
        coverage_pct = round((papers_with_country / total_papers) * 100, 2) if total_papers > 0 else 0.0

        frequency_list = [
            {
                "country": country,
                "iso_a3": get_country_iso3(country),
                "frequency": int(count),
                "percentage": round((count / total_papers) * 100, 2) if total_papers > 0 else 0.0,
            }
            for country, count in country_paper_counts.most_common()
        ]

        collaboration_edges = [
            {
                "source": source,
                "target": target,
                "weight": int(weight),
            }
            for (source, target), weight in collaboration_counts.most_common()
            if weight > 0
        ]

        nodes = [
            {
                "id": country,
                "label": country,
                "iso_a3": get_country_iso3(country),
                "paper_count": int(count),
            }
            for country, count in country_paper_counts.most_common()
        ]

        links = [
            {
                "source": source,
                "target": target,
                "weight": int(weight),
            }
            for (source, target), weight in collaboration_counts.most_common()
            if weight > 0
        ]

        computed = {
            "source_file": filename,
            "filename": filename,
            "total_papers": total_papers,
            "papers_with_country_data": papers_with_country,
            "papers_without_country_data": papers_without_country,
            "unique_countries": len(country_paper_counts),
            "international_papers": international_papers,
            "country_coverage_percentage": coverage_pct,
            "country_frequency": frequency_list,
            "collaboration_edges": collaboration_edges,
            "nodes": nodes,
            "links": links,
            "unassigned_papers": unassigned_papers,
        }

        if cache_key and abs_path:
            stale_keys = [k for k in self._CACHE if k[0] == abs_path]
            for k in stale_keys:
                del self._CACHE[k]
            self._CACHE[cache_key] = computed

        return computed

    def analyze_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform country frequency and international collaboration network analysis on a list of paper records.
        """
        return self._compute_metrics_from_records(records)

    def analyze_csv(self, csv_path: str, exclude_duplicates: bool = True) -> Dict[str, Any]:
        """
        Load a CSV using canonical loader and perform country analysis.
        By default exclude_duplicates=True so duplicate records do not distort country distribution.
        Reuses cached result if available.
        """
        return self._get_or_compute_analysis(csv_path, exclude_duplicates=exclude_duplicates)

    def get_collaboration_graph_from_records(
        self, records: List[Dict[str, Any]], filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build country-level research collaboration graph from paper records.
        Returns graph format with 'nodes' (id, label, paper_count) and 'links' (source, target, weight).
        """
        res = self.analyze_records(records)
        return {
            "filename": filename or "",
            "nodes": res["nodes"],
            "links": res["links"],
            "total_papers": res["total_papers"],
            "papers_with_country_data": res["papers_with_country_data"],
            "papers_without_country_data": res["papers_without_country_data"],
            "international_papers": res["international_papers"],
            "country_coverage_percentage": res["country_coverage_percentage"],
        }

    def get_collaboration_graph_from_csv(self, csv_path: str, exclude_duplicates: bool = True) -> Dict[str, Any]:
        """
        Load CSV using canonical loader and compute country collaboration graph.
        By default exclude_duplicates=True so duplicate records do not distort collaboration networks.
        Reuses cached result if available.
        """
        data = self._get_or_compute_analysis(csv_path, exclude_duplicates=exclude_duplicates)
        return {
            "filename": data["filename"],
            "nodes": data["nodes"],
            "links": data["links"],
            "total_papers": data["total_papers"],
            "papers_with_country_data": data["papers_with_country_data"],
            "papers_without_country_data": data["papers_without_country_data"],
            "international_papers": data["international_papers"],
            "country_coverage_percentage": data["country_coverage_percentage"],
        }



