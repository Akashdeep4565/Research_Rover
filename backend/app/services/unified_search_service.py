"""
Unified Search Service for Research Rover.

Orchestrates multi-source search across PubMed and OpenAlex, performing
field normalization, intelligent deduplication, and paper record merging.
"""

import asyncio
from datetime import date
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from app.core.config import Settings
from app.models.schemas import SearchSource
from app.services.openalex_service import OpenAlexService
from app.services.pubmed_service import PubMedService

logger = logging.getLogger("research_rover")

re_doi_prefix = re.compile(r"^https?://(?:dx\.)?doi\.org/", re.IGNORECASE)
re_non_alpha = re.compile(r"[^a-z0-9]", re.IGNORECASE)


class UnifiedSearchService:
    """Orchestrator for unified multi-source paper searches."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.openalex_service = OpenAlexService(settings)
        self.last_warning: Optional[str] = None

    @staticmethod
    def normalize_doi(doi: Any) -> str:
        """Normalize DOI string for matching."""
        if not doi:
            return ""
        s = str(doi).strip().lower()
        s = re_doi_prefix.sub("", s)
        return s.strip()

    @staticmethod
    def normalize_pmid(pmid: Any) -> str:
        """Normalize PMID string for matching."""
        if not pmid:
            return ""
        s = str(pmid).strip()
        if "/" in s:
            s = s.rstrip("/").split("/")[-1]
        return s.strip()

    @staticmethod
    def normalize_openalex_id(openalex_id: Any) -> str:
        """Normalize OpenAlex ID for matching."""
        if not openalex_id:
            return ""
        s = str(openalex_id).strip()
        return s

    @staticmethod
    def compute_title_key(title: Any, year: Any, first_author: Any) -> str:
        """Construct fallback key from normalized title, year, and first author."""
        if not title:
            return ""
        norm_title = re_non_alpha.sub("", str(title).lower())
        if len(norm_title) < 8:
            return ""
        norm_year = str(year or "").strip()
        norm_author = ""
        if isinstance(first_author, str) and first_author.strip():
            norm_author = re_non_alpha.sub("", first_author.lower())
        elif isinstance(first_author, list) and first_author:
            norm_author = re_non_alpha.sub("", str(first_author[0]).lower())

        return f"{norm_title[:60]}_{norm_year}_{norm_author[:20]}"

    def merge_paper_records(self, rec1: Dict[str, Any], rec2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two duplicate paper records from different sources (e.g. PubMed + OpenAlex).
        Preserves identifiers, sources list, and combines complementary metadata.
        """
        # Determine source tags
        s1 = rec1.get("sources") or [rec1.get("source") or rec1.get("Source") or "unknown"]
        s2 = rec2.get("sources") or [rec2.get("source") or rec2.get("Source") or "unknown"]
        if isinstance(s1, str):
            s1 = [s1]
        if isinstance(s2, str):
            s2 = [s2]

        merged_sources = list(dict.fromkeys(s1 + s2))

        # Title: prefer longer/more informative title
        t1 = str(rec1.get("Title") or rec1.get("title") or "")
        t2 = str(rec2.get("Title") or rec2.get("title") or "")
        title = t1 if len(t1) >= len(t2) else t2

        # Abstract: prefer non-empty / longer abstract
        a1 = str(rec1.get("Abstract") or rec1.get("abstract") or "")
        a2 = str(rec2.get("Abstract") or rec2.get("abstract") or "")
        abstract = a1 if len(a1) >= len(a2) else a2

        # Identifiers
        doi = self.normalize_doi(rec1.get("DOI") or rec1.get("doi")) or self.normalize_doi(rec2.get("DOI") or rec2.get("doi"))
        pmid = self.normalize_pmid(rec1.get("PMID") or rec1.get("pmid")) or self.normalize_pmid(rec2.get("PMID") or rec2.get("pmid"))
        openalex_id = self.normalize_openalex_id(rec1.get("OpenAlex_ID") or rec1.get("openalex_id")) or self.normalize_openalex_id(rec2.get("OpenAlex_ID") or rec2.get("openalex_id"))

        # Year and Publication Date
        year = str(rec1.get("Publication Year") or rec1.get("year") or rec2.get("Publication Year") or rec2.get("year") or "")

        # Authors
        auth1 = rec1.get("Authors") or rec1.get("authors") or []
        auth2 = rec2.get("Authors") or rec2.get("authors") or []
        if isinstance(auth1, str): auth1 = [auth1]
        if isinstance(auth2, str): auth2 = [auth2]
        merged_authors = list(dict.fromkeys([a for a in (auth1 + auth2) if a and str(a).strip()]))

        # Affiliations and Countries
        aff1 = rec1.get("Affiliations") or rec1.get("affiliations") or ""
        aff2 = rec2.get("Affiliations") or rec2.get("affiliations") or ""
        if isinstance(aff1, list): aff1 = "; ".join(aff1)
        if isinstance(aff2, list): aff2 = "; ".join(aff2)
        merged_aff = "; ".join(filter(None, dict.fromkeys([str(aff1).strip(), str(aff2).strip()])))

        c1 = rec1.get("Countries") or rec1.get("countries") or []
        c2 = rec2.get("Countries") or rec2.get("countries") or []
        if isinstance(c1, str): c1 = [c1]
        if isinstance(c2, str): c2 = [c2]
        merged_countries = sorted(list(dict.fromkeys([c for c in (c1 + c2) if c and str(c).strip()])))

        # Keywords
        kw1 = rec1.get("Keywords") or rec1.get("keywords") or []
        kw2 = rec2.get("Keywords") or rec2.get("keywords") or []
        if isinstance(kw1, str): kw1 = [kw1]
        if isinstance(kw2, str): kw2 = [kw2]
        merged_keywords = list(dict.fromkeys([k for k in (kw1 + kw2) if k and str(k).strip()]))

        # URLs
        url1 = rec1.get("Download_URL") or rec1.get("download_url") or ""
        url2 = rec2.get("Download_URL") or rec2.get("download_url") or ""
        url = url1 or url2

        # PDF URLs: prefer verified direct PDF URL (.pdf direct link over repository landing/stream)
        pdf1 = str(rec1.get("PDF_URL") or rec1.get("pdf_url") or "").strip()
        pdf2 = str(rec2.get("PDF_URL") or rec2.get("pdf_url") or "").strip()

        def _pdf_priority(u: str) -> int:
            if not u:
                return 0
            u_clean = u.lower().split("?")[0]
            if u_clean.endswith(".pdf"):
                return 3  # Direct .pdf file link
            if "/pdf/" in u.lower() or u.lower().endswith("/pdf"):
                return 2  # PMC / repository viewer stream path
            return 1

        p1, p2 = _pdf_priority(pdf1), _pdf_priority(pdf2)
        if p2 > p1:
            merged_pdf_url = pdf2
        elif p1 > p2:
            merged_pdf_url = pdf1
        else:
            merged_pdf_url = pdf1 or pdf2

        merged_is_oa = bool(
            rec1.get("Is_OA") or rec1.get("is_oa") or
            rec2.get("Is_OA") or rec2.get("is_oa") or
            merged_pdf_url
        )

        # Source String Display
        source_str = "pubmed, openalex" if len(merged_sources) > 1 else merged_sources[0]

        return {
            "Source": source_str,
            "source": source_str,
            "sources": merged_sources,
            "Title": title,
            "title": title,
            "DOI": doi,
            "doi": doi,
            "PMID": pmid,
            "pmid": pmid,
            "OpenAlex_ID": openalex_id,
            "openalex_id": openalex_id,
            "Abstract": abstract,
            "abstract": abstract,
            "Publication Year": year,
            "year": year,
            "Authors": merged_authors,
            "authors": merged_authors,
            "Affiliations": merged_aff,
            "affiliations": merged_aff,
            "Countries": merged_countries,
            "countries": merged_countries,
            "Keywords": merged_keywords,
            "keywords": merged_keywords,
            "Download_URL": url,
            "download_url": url,
            "PDF_URL": merged_pdf_url or None,
            "pdf_url": merged_pdf_url or None,
            "Citation_Count": max(int(rec1.get("Citation_Count") or rec1.get("citation_count") or 0), int(rec2.get("Citation_Count") or rec2.get("citation_count") or 0)),
            "citation_count": max(int(rec1.get("Citation_Count") or rec1.get("citation_count") or 0), int(rec2.get("Citation_Count") or rec2.get("citation_count") or 0)),
            "Is_OA": merged_is_oa,
            "is_oa": merged_is_oa,
            "Relevance_Score": rec1.get("Relevance_Score") or rec2.get("Relevance_Score"),
            "relevance_score": rec1.get("relevance_score") or rec2.get("relevance_score"),
        }

    def deduplicate_results(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate candidate records matching by DOI, PMID, OpenAlex ID, or Title+Year+Author.
        Preserves original records while merging duplicate paper representations.
        """
        if not records:
            return []

        doi_index: Dict[str, int] = {}
        pmid_index: Dict[str, int] = {}
        openalex_index: Dict[str, int] = {}
        title_index: Dict[str, int] = {}

        unique_list: List[Dict[str, Any]] = []

        for rec in records:
            doi = self.normalize_doi(rec.get("DOI") or rec.get("doi"))
            pmid = self.normalize_pmid(rec.get("PMID") or rec.get("pmid"))
            openalex_id = self.normalize_openalex_id(rec.get("OpenAlex_ID") or rec.get("openalex_id"))

            authors = rec.get("Authors") or rec.get("authors") or []
            title_key = self.compute_title_key(
                rec.get("Title") or rec.get("title"),
                rec.get("Publication Year") or rec.get("year"),
                authors[0] if authors else "",
            )

            matched_idx: Optional[int] = None

            # Priority 1: DOI Match
            if doi and doi in doi_index:
                matched_idx = doi_index[doi]
            # Priority 2: PMID Match
            elif pmid and pmid in pmid_index:
                matched_idx = pmid_index[pmid]
            # Priority 3: OpenAlex ID Match
            elif openalex_id and openalex_id in openalex_index:
                matched_idx = openalex_index[openalex_id]
            # Priority 4: Title + Year + Author Match
            elif title_key and title_key in title_index:
                matched_idx = title_index[title_key]

            if matched_idx is not None:
                # Merge duplicate into existing record
                existing = unique_list[matched_idx]
                merged = self.merge_paper_records(existing, rec)
                unique_list[matched_idx] = merged

                # Update index lookups with merged identifiers
                if doi: doi_index[doi] = matched_idx
                if pmid: pmid_index[pmid] = matched_idx
                if openalex_id: openalex_index[openalex_id] = matched_idx
                if title_key: title_index[title_key] = matched_idx
            else:
                new_idx = len(unique_list)
                # Ensure record has normalized source fields
                rec_copy = dict(rec)
                src = rec_copy.get("Source") or rec_copy.get("source") or "unknown"
                rec_copy["source"] = src
                rec_copy["Source"] = src
                rec_copy["sources"] = [src]

                unique_list.append(rec_copy)

                if doi: doi_index[doi] = new_idx
                if pmid: pmid_index[pmid] = new_idx
                if openalex_id: openalex_index[openalex_id] = new_idx
                if title_key: title_index[title_key] = new_idx

        return unique_list

    def deduplicate_and_merge(
        self, pubmed_records: List[Dict[str, Any]], openalex_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Alias for deduplicate_results accepting two separate record lists."""
        return self.deduplicate_results((pubmed_records or []) + (openalex_records or []))

    async def execute_search(
        self,
        query: str,
        max_results: int = 10,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        search_source: Union[SearchSource, str] = SearchSource.UNIFIED,
        use_raw_query: bool = False,
        cancel_event: Optional[Any] = None,
        pubmed_fetch_fn: Optional[Any] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute paper search across PubMed, OpenAlex, or Unified Search.
        Handles non-blocking partial failures if one external API fails.
        """
        self.last_warning = None
        source_str = (
            search_source.value if isinstance(search_source, SearchSource) else str(search_source).lower()
        )

        # 1. PubMed Only
        if source_str == "pubmed":
            if not pubmed_fetch_fn:
                return []
            return await pubmed_fetch_fn(query, max_results, start_date, end_date, use_raw_query, cancel_event)

        # 2. OpenAlex Only
        if source_str == "openalex":
            return await self.openalex_service.search_works(
                query=query,
                max_results=max_results,
                start_date=start_date,
                end_date=end_date,
                cancel_event=cancel_event,
            )

        # 3. Unified Search (PubMed + OpenAlex)
        logger.info(f"Executing Unified Search (PubMed + OpenAlex) for query: '{query}'")

        pubmed_task = None
        if pubmed_fetch_fn:
            pubmed_task = asyncio.create_task(
                pubmed_fetch_fn(query, max_results, start_date, end_date, use_raw_query, cancel_event)
            )

        openalex_task = asyncio.create_task(
            self.openalex_service.search_works(
                query=query,
                max_results=max_results,
                start_date=start_date,
                end_date=end_date,
                cancel_event=cancel_event,
            )
        )

        pubmed_results: List[Dict[str, Any]] = []
        openalex_results: List[Dict[str, Any]] = []

        pubmed_err: Optional[Exception] = None
        openalex_err: Optional[Exception] = None

        if pubmed_task:
            try:
                pubmed_results = await pubmed_task
            except Exception as e:
                logger.error(f"PubMed search failed in Unified Search: {e}")
                pubmed_err = e

        try:
            openalex_results = await openalex_task
        except Exception as e:
            logger.error(f"OpenAlex search failed in Unified Search: {e}")
            openalex_err = e

        # Handle non-blocking partial failures
        if pubmed_err and not openalex_err:
            self.last_warning = "PubMed could not be reached. OpenAlex results are displayed."
            logger.warning(self.last_warning)
        elif openalex_err and not pubmed_err:
            self.last_warning = "OpenAlex could not be reached. PubMed results are displayed."
            logger.warning(self.last_warning)
        elif pubmed_err and openalex_err:
            logger.error("Both PubMed and OpenAlex queries failed in Unified Search.")
            raise Exception("Failed to retrieve search results from PubMed and OpenAlex.")

        combined_raw = (pubmed_results or []) + (openalex_results or [])
        logger.info(f"Unified Search collected {len(pubmed_results)} PubMed papers and {len(openalex_results)} OpenAlex papers")

        deduped = self.deduplicate_results(combined_raw)
        logger.info(f"Unified Search deduplicated {len(combined_raw)} records down to {len(deduped)} papers")

        return deduped


from typing import Union
