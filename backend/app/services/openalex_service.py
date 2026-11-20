"""
OpenAlex Service for Research Rover.

Integrates with the official OpenAlex REST API (https://api.openalex.org/works)
to retrieve open research literature, authors, affiliations, countries, and topic concepts.
"""

from datetime import date
import logging
import os
import time
from typing import Any, Dict, List, Optional
import urllib.parse
import httpx

from app.core.config import Settings
from app.utils.country_extractor import extract_countries_from_affiliations

logger = logging.getLogger("research_rover")

OPENALEX_WORKS_URL = "https://api.openalex.org/works"


class OpenAlexService:
    """Service for querying OpenAlex API and parsing works metadata."""

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings
        # Read API key safely from settings or environment without logging secrets
        self.api_key = (
            getattr(settings, "OPENALEX_API_KEY", "")
            or os.environ.get("OPENALEX_API_KEY", "")
        ).strip()
        self.email = (
            getattr(settings, "EMAIL", "") or "researchrover@example.com"
        ).strip()

    def _get_headers_and_params(
        self,
        query: str,
        max_results: int = 10,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> tuple[Dict[str, str], Dict[str, Any]]:
        """Construct headers and query parameters for OpenAlex request."""
        user_agent = f"ResearchRover/2.0 (mailto:{self.email})"
        headers = {"User-Agent": user_agent}

        params: Dict[str, Any] = {
            "search": query,
            "per_page": min(max(1, max_results), 200),
            "mailto": self.email,
        }

        if self.api_key:
            params["api_key"] = self.api_key

        # Construct date filters if provided
        filters = []
        if start_date:
            filters.append(f"from_publication_date:{start_date.strftime('%Y-%m-%d')}")
        if end_date:
            filters.append(f"to_publication_date:{end_date.strftime('%Y-%m-%d')}")

        if filters:
            params["filter"] = ",".join(filters)

        return headers, params

    @staticmethod
    def reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
        """
        Reconstruct abstract plain text from OpenAlex abstract_inverted_index.
        Format: {"word": [position_index1, position_index2]}
        """
        if not inverted_index or not isinstance(inverted_index, dict):
            return ""

        try:
            pos_map: Dict[int, str] = {}
            for word, positions in inverted_index.items():
                if isinstance(positions, list):
                    for pos in positions:
                        pos_map[pos] = word

            sorted_positions = sorted(pos_map.keys())
            return " ".join([pos_map[pos] for pos in sorted_positions]).strip()
        except Exception as e:
            logger.debug(f"Failed to reconstruct abstract from inverted index: {e}")
            return ""

    @staticmethod
    def extract_clean_doi(raw_doi: Optional[str]) -> str:
        """Standardize DOI string by stripping url prefixes."""
        if not raw_doi:
            return ""
        s = str(raw_doi).strip()
        s = re_doi_prefix.sub("", s)
        return s.strip()

    @staticmethod
    def extract_clean_pmid(ids_dict: Optional[Dict[str, Any]]) -> str:
        """Extract clean PMID string from OpenAlex ids object."""
        if not ids_dict or not isinstance(ids_dict, dict):
            return ""
        pmid_val = ids_dict.get("pmid")
        if not pmid_val:
            return ""
        s = str(pmid_val).strip()
        # Remove URL prefix if present e.g. https://pubmed.ncbi.nlm.nih.gov/12345678
        if "/" in s:
            s = s.rstrip("/").split("/")[-1]
        return s.strip()

    def parse_work_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw OpenAlex work item into standard Research Rover paper dictionary.
        Preserves OpenAlex-specific metadata while providing common display attributes.
        """
        openalex_id = str(item.get("id") or "").strip()
        if "/" in openalex_id:
            openalex_id = openalex_id.rstrip("/").split("/")[-1]
        title = str(item.get("title") or "Unknown Title").strip()

        # Abstract reconstruction
        abstract = self.reconstruct_abstract(item.get("abstract_inverted_index"))

        # DOI and PMID
        raw_doi = item.get("doi")
        doi = self.extract_clean_doi(raw_doi)
        pmid = self.extract_clean_pmid(item.get("ids"))

        # Publication Year & Date
        pub_year = str(item.get("publication_year") or "")
        pub_date = str(item.get("publication_date") or "")

        # Source / Journal / Location
        primary_loc = item.get("primary_location") or {}
        best_oa = item.get("best_oa_location") or {}
        loc_source = primary_loc.get("source") or best_oa.get("source") or {}
        journal = str(loc_source.get("display_name") or "").strip() or "OpenAlex"
        landing_page_url = str(primary_loc.get("landing_page_url") or best_oa.get("landing_page_url") or "").strip()

        # Prioritize verified direct PDF URL from OpenAlex locations
        pdf_url = ""
        if best_oa.get("pdf_url"):
            pdf_url = str(best_oa["pdf_url"]).strip()
        elif primary_loc.get("pdf_url"):
            pdf_url = str(primary_loc["pdf_url"]).strip()
        else:
            for loc in (item.get("locations") or []):
                if isinstance(loc, dict) and loc.get("pdf_url"):
                    pdf_url = str(loc["pdf_url"]).strip()
                    break

        # Open Access info
        oa_info = item.get("open_access") or {}
        is_oa = bool(oa_info.get("is_oa", False))
        if not pdf_url:
            oa_url = str(oa_info.get("oa_url") or "").strip()
            if oa_url:
                if oa_url.lower().endswith(".pdf") or "/pdf" in oa_url.lower():
                    pdf_url = oa_url
                elif not landing_page_url:
                    landing_page_url = oa_url

        # Check for PMCID in OpenAlex ids
        ids = item.get("ids") or {}
        pmcid = str(ids.get("pmcid") or "").strip()
        if not pdf_url and pmcid:
            clean_pmc = pmcid if pmcid.upper().startswith("PMC") else f"PMC{pmcid}"
            pdf_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{clean_pmc}/pdf/"
            is_oa = True

        if pdf_url:
            is_oa = True

        # Authors, Institutions, and Countries
        authors: List[str] = []
        author_ids: List[str] = []
        institutions: List[str] = []
        raw_affiliations: List[str] = []
        countries_set: set[str] = set()

        authorships = item.get("authorships") or []
        for authorship in authorships:
            if not isinstance(authorship, dict):
                continue

            # Author name
            author_obj = authorship.get("author") or {}
            author_name = str(author_obj.get("display_name") or "").strip()
            if author_name:
                authors.append(author_name)
            if author_obj.get("id"):
                author_ids.append(str(author_obj.get("id")))

            # Raw affiliation strings
            raw_strings = authorship.get("raw_affiliation_strings") or []
            for raw_str in raw_strings:
                if raw_str and str(raw_str).strip():
                    raw_affiliations.append(str(raw_str).strip())
                    # Extract countries from raw affiliation string using Country Extractor
                    for c in extract_countries_from_affiliations(str(raw_str)):
                        countries_set.add(c)

            # Institutions & Countries
            inst_list = authorship.get("institutions") or []
            for inst in inst_list:
                if isinstance(inst, dict):
                    inst_name = str(inst.get("display_name") or "").strip()
                    country_code = str(inst.get("country_code") or "").strip()
                    if inst_name:
                        institutions.append(inst_name)
                        if country_code:
                            raw_affiliations.append(f"{inst_name}, {country_code}")
                        else:
                            raw_affiliations.append(inst_name)

                    # Extract country from institution object
                    if country_code:
                        for c in extract_countries_from_affiliations(country_code):
                            countries_set.add(c)
                        for c in extract_countries_from_affiliations(inst_name):
                            countries_set.add(c)

            # Explicit countries list in authorship
            c_codes = authorship.get("countries") or []
            for cc in c_codes:
                if cc and str(cc).strip():
                    for c in extract_countries_from_affiliations(str(cc)):
                        countries_set.add(c)

        # Concepts / Topics / Keywords
        concepts: List[str] = []
        concepts_list = item.get("concepts") or []
        for conc in concepts_list:
            if isinstance(conc, dict) and conc.get("display_name"):
                concepts.append(str(conc.get("display_name")).strip())

        topics_list = item.get("topics") or []
        for top in topics_list:
            if isinstance(top, dict) and top.get("display_name"):
                concepts.append(str(top.get("display_name")).strip())

        # Deduplicate list fields while preserving order
        unique_authors = list(dict.fromkeys(authors))
        unique_affiliations = list(dict.fromkeys(raw_affiliations))
        unique_countries = sorted(list(countries_set))
        unique_keywords = list(dict.fromkeys(concepts))

        # Construct paper record dictionary
        return {
            "Source": "openalex",
            "source": "openalex",
            "openalex_id": openalex_id,
            "OpenAlex_ID": openalex_id,
            "pmid": pmid,
            "PMID": pmid,
            "Title": title,
            "title": title,
            "DOI": doi,
            "doi": doi,
            "Abstract": abstract,
            "abstract": abstract,
            "Publication Year": pub_year,
            "Publication_Date": pub_date,
            "year": pub_year,
            "Journal": journal,
            "source_journal": journal,
            "Authors": unique_authors,
            "authors": unique_authors,
            "Affiliations": "; ".join(unique_affiliations) if unique_affiliations else "",
            "affiliations": unique_affiliations,
            "countries": unique_countries,
            "Countries": unique_countries,
            "Keywords": unique_keywords,
            "keywords": unique_keywords,
            "Citation_Count": int(item.get("cited_by_count") or 0),
            "citation_count": int(item.get("cited_by_count") or 0),
            "Is_OA": is_oa,
            "is_oa": is_oa,
            "Download_URL": landing_page_url or pdf_url or (f"https://doi.org/{doi}" if doi else ""),
            "download_url": landing_page_url or pdf_url or (f"https://doi.org/{doi}" if doi else ""),
            "pdf_url": pdf_url or None,
            "PDF_URL": pdf_url or None,
            "landing_page_url": landing_page_url,
            "type": str(item.get("type") or "article"),
            "raw_openalex": {
                "id": openalex_id,
                "type": item.get("type"),
                "cited_by_count": item.get("cited_by_count"),
                "is_oa": is_oa,
                "institution_ids": list(dict.fromkeys(author_ids)),
            },
        }

    def _parse_work(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Alias for parse_work_item."""
        return self.parse_work_item(item)

    async def search_papers(
        self,
        query: str,
        max_results: int = 10,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        cancel_event: Optional[Any] = None,
    ) -> List[Dict[str, Any]]:
        """Alias for search_works to match SearchService convention."""
        return await self.search_works(
            query=query,
            max_results=max_results,
            start_date=start_date,
            end_date=end_date,
            cancel_event=cancel_event,
        )

    async def search_works(
        self,
        query: str,
        max_results: int = 10,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        cancel_event: Optional[Any] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search OpenAlex works API for research papers matching the query.
        Handles retries, rate limiting, and timeouts gracefully.
        """
        if not query or not query.strip():
            return []

        headers, params = self._get_headers_and_params(
            query=query.strip(),
            max_results=max_results,
            start_date=start_date,
            end_date=end_date,
        )

        max_retries = 3
        backoff = 1.0

        for attempt in range(1, max_retries + 1):
            if cancel_event and getattr(cancel_event, "is_set", lambda: False)():
                logger.info("OpenAlex search cancelled before HTTP request")
                return []

            try:
                logger.info(f"Querying OpenAlex API (attempt {attempt}/{max_retries}) for query: '{query}'")

                async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
                    response = await client.get(OPENALEX_WORKS_URL, headers=headers, params=params)

                # Handle Rate Limiting (429)
                if response.status_code == 429:
                    logger.warning(f"OpenAlex rate limit (429) hit. Backing off for {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2
                    continue

                response.raise_for_status()
                data = response.json()

                results_list = data.get("results") or []
                logger.info(f"OpenAlex API returned {len(results_list)} raw work items")

                parsed_papers: List[Dict[str, Any]] = []
                for item in results_list:
                    if not isinstance(item, dict):
                        continue
                    try:
                        parsed = self.parse_work_item(item)
                        if parsed and parsed.get("Title"):
                            parsed_papers.append(parsed)
                    except Exception as parse_err:
                        logger.warning(f"Error parsing single OpenAlex work record: {parse_err}")
                        continue

                return parsed_papers

            except httpx.HTTPStatusError as http_err:
                logger.error(f"OpenAlex HTTP error status {http_err.response.status_code}: {http_err.response.text[:200]}")
                if attempt == max_retries:
                    return []
                time.sleep(backoff)
                backoff *= 2
            except httpx.RequestError as req_err:
                logger.error(f"OpenAlex request connection/timeout error: {req_err}")
                if attempt == max_retries:
                    return []
                time.sleep(backoff)
                backoff *= 2
            except Exception as e:
                logger.error(f"Unexpected error during OpenAlex search: {e}")
                return []

        return []


import re
re_doi_prefix = re.compile(r"^https?://(?:dx\.)?doi\.org/", re.IGNORECASE)
