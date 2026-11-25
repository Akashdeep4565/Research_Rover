"""
Optimized PubMed searcher for Research Rover
Fixed version: uses proper MeSH[MH] field tagging, removes broken score filter
"""

from datetime import date
import requests
from requests.adapters import HTTPAdapter
import pandas as pd
import time
import logging
from typing import Optional, List, Dict, Any, Tuple, Set, Callable
from xml.etree import ElementTree as ET
import re

logger = logging.getLogger("research_rover")


# ---------------------------------------------------------------------------
# Synonym map — manual fallback used when MeSH lookup returns nothing
# ---------------------------------------------------------------------------
SYNONYM_MAP: Dict[str, List[str]] = {
    "smart healthcare": [
        "digital health", "ehealth", "e-health", "mhealth", "m-health",
        "connected health", "health informatics", "medical informatics",
        "telemedicine", "telehealth", "smart health",
    ],
    "machine learning": [
        "deep learning", "neural network", "artificial intelligence",
        "ai", "ml", "random forest", "support vector machine",
        "natural language processing", "nlp",
    ],
    "software industry": [
        "software development", "software engineering", "it industry",
        "software company", "tech industry", "information technology",
    ],
    "internet of things": [
        "iot", "iiot", "connected devices", "sensor network",
        "smart devices", "wearable",
    ],
    "electronic health records": [
        "ehr", "emr", "electronic medical records", "clinical data",
    ],
    "blockchain": [
        "distributed ledger", "block chain", "smart contract",
    ],
    "big data": [
        "data analytics", "data mining", "large scale data",
    ],
    "cloud computing": [
        "cloud storage", "cloud platform", "saas", "paas",
    ],
}

# ---------------------------------------------------------------------------
# Relevant journal whitelist
# ---------------------------------------------------------------------------
RELEVANT_JOURNALS = [
    "journal of medical internet research",
    "npj digital medicine",
    "ieee journal of biomedical",
    "computers in biology and medicine",
    "health informatics journal",
    "journal of biomedical informatics",
    "international journal of medical informatics",
    "telemedicine and e-health",
    "digital health",
    "applied clinical informatics",
    "jmir",
]

# ---------------------------------------------------------------------------
# Retry config
# ---------------------------------------------------------------------------
MAX_RETRIES = 3
RETRY_BACKOFF = [1, 3, 7]


class PubMedService:
    """Optimized PubMed searcher with rate limiting and batch processing"""

    def __init__(self, email: str, api_key: Optional[str] = None):
        self.email = email
        self.api_key = api_key
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.rate_limit = 0.1  # 10 requests/sec with API key
        if not api_key:
            self.rate_limit = 0.34  # 3 requests/sec without API key

        # Connection pool with HTTP keep-alive
        self.session = requests.Session()
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=0)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update({"User-Agent": f"ResearchRover/2.0 ({self.email})"})

        # Set when a zero-result search succeeds after ESpell correction,
        # so callers can tell the user "showing results for <corrected>".
        self.last_corrected_query: Optional[str] = None

        # Tracking for retrieval completeness and partial failures
        self._failed_pmids: List[str] = []
        self._failed_batches_count: int = 0
        self.last_retrieval_report: Dict[str, Any] = {}

        # PMC enrichment tracking & circuit breaker
        self._pmc_attempted_pmids: Set[str] = set()
        self._pmc_circuit_broken: bool = False
        self._pmc_consecutive_failures: int = 0
        self.MAX_PMC_CONSECUTIVE_FAILURES: int = 2
        self.last_enrichment_warning: Optional[str] = None

    def close(self) -> None:
        """Close the underlying requests Session."""
        try:
            self.session.close()
        except Exception:
            pass

    def __del__(self) -> None:
        self.close()

    # ------------------------------------------------------------------
    # HTTP helper — POST with retry/backoff
    # ------------------------------------------------------------------

    def _post_with_retry(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """POST to a PubMed endpoint with exponential backoff on transient errors."""
        url = f"{self.base_url}{endpoint}"
        data = dict(data)
        data['email'] = self.email
        if self.api_key:
            data['api_key'] = self.api_key

        # efetch.fcgi and esummary.fcgi retries are managed by the batch handler to eliminate nested retry multiplication.
        # esearch.fcgi and espell.fcgi use MAX_RETRIES.
        retries = 1 if endpoint in ('efetch.fcgi', 'esummary.fcgi') else MAX_RETRIES
        timeout = 15 if endpoint == 'esummary.fcgi' else 30

        last_exc: Optional[Exception] = None
        for attempt in range(retries):
            try:
                time.sleep(self.rate_limit)
                response = self.session.post(url, data=data, timeout=timeout)
                if response.status_code in (429, 500, 502, 503, 504):
                    wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                    logger.warning(
                        f"PubMed {endpoint} returned {response.status_code} "
                        f"(attempt {attempt+1}/{retries}), retrying in {wait}s"
                    )
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                last_exc = e
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                logger.warning(
                    f"PubMed {endpoint} request error (attempt {attempt+1}/{retries}): "
                    f"{e}, retrying in {wait}s"
                )
                time.sleep(wait)

        raise RuntimeError(
            f"PubMed {endpoint} failed after {retries} attempts. Last error: {last_exc}"
        )

    # ------------------------------------------------------------------
    # Spelling correction — PubMed's ESpell service
    # ------------------------------------------------------------------

    def _spell_check(self, query: str) -> Optional[str]:
        """
        Ask PubMed's ESpell service for a corrected spelling of the query.

        This is the same engine behind the "Did you mean ...?" suggestion on
        the PubMed website, and it understands biomedical vocabulary (drug
        names, procedures, etc.) that a generic spell-checker would mangle.

        Returns the corrected query string only when PubMed suggests a
        spelling that differs from the input; otherwise None.
        """
        term = (query or "").strip()
        if not term:
            return None
        try:
            response = self._post_with_retry(
                'espell.fcgi', {'db': 'pubmed', 'term': term}
            )
            root = ET.fromstring(response.content)
            corrected_elem = root.find('.//CorrectedQuery')
            if corrected_elem is not None and corrected_elem.text:
                corrected = corrected_elem.text.strip()
                if corrected and corrected.lower() != term.lower():
                    logger.info(f"ESpell suggests '{corrected}' for '{term}'")
                    return corrected
            logger.info(f"ESpell found no correction for '{term}'")
            return None
        except Exception as e:
            logger.warning(f"ESpell lookup failed for '{term}': {e}")
            return None

    # ------------------------------------------------------------------
    # Synonym + MeSH expansion
    # ------------------------------------------------------------------

    def _get_synonyms(self, term: str) -> List[str]:
        """Return manual synonyms from SYNONYM_MAP (exact match only)."""
        return SYNONYM_MAP.get(term.lower().strip(), [])

    def _build_expanded_query_for_term(self, term: str) -> str:
        """
        Build a PubMed sub-query for a single concept, leaning on PubMed's
        **Automatic Term Mapping (ATM)** rather than hand-fetching MeSH (the old
        MeSH-database lookup was both broken — it parsed plain text as XML — and
        unreliable, returning subtypes like "Donohue Syndrome" for "diabetes").

        Per concept, plus every manual ``SYNONYM_MAP`` entry, we emit a clause
        via :meth:`_concept_clause`:

          - **Single word** (e.g. ``hypertension``) → left *untagged* so ATM maps
            it to the right MeSH descriptor + entry-term synonyms + spelling
            variants. A lone word can't be mis-split, so this is pure upside.
          - **Multi-word** (e.g. ``screen time``) → ``("screen time"[MeSH Terms]
            OR "screen time")``: keeps the exact phrase (so ATM doesn't dissolve
            it into ``screen AND time`` and drag in unrelated papers) while still
            matching everything PubMed tagged with that MeSH descriptor. If the
            phrase isn't a MeSH descriptor the ``[MeSH Terms]`` clause simply
            matches nothing (PubMed warns; harmless inside an OR).

        Result looks like:
          ``(("screen time"[MeSH Terms] OR "screen time") OR "screen use" ...)``
        """
        term = term.strip()

        seen, clauses = set(), []
        for v in [term] + self._get_synonyms(term):
            key = v.lower().strip()
            if key and key not in seen:
                seen.add(key)
                clause = self._concept_clause(v)
                if clause:
                    clauses.append(clause)

        if not clauses:
            return term

        built = clauses[0] if len(clauses) == 1 else "(" + " OR ".join(clauses) + ")"
        logger.info(f"Expanded query for '{term}': {len(clauses)} clause(s) -> {built}")
        return built

    @staticmethod
    def _concept_clause(phrase: str) -> str:
        """Build one OR-clause for a concept/synonym (see _build_expanded_query_for_term)."""
        phrase = phrase.strip().strip('"').strip()
        if not phrase:
            return ""
        if " " in phrase:
            # Multi-word: exact phrase + MeSH descriptor, no ATM word-splitting.
            return f'("{phrase}"[MeSH Terms] OR "{phrase}")'
        # Single token: bare, so ATM expands it fully (MeSH + synonyms + variants).
        return phrase

    # ------------------------------------------------------------------
    # Main search entry point
    # ------------------------------------------------------------------

    def search_and_retrieve_optimized(
        self,
        query: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        max_results: int = 1000,
        use_raw_query: bool = False,
        cancel_event: Optional[Any] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> pd.DataFrame:
        """
        Search PubMed and retrieve paper details.

        Query strategy (use_raw_query=False, default):
          1. Split user query into individual terms (comma-separated)
          2. For each term, build an expanded sub-query combining
             [Title/Abstract] variants and [MeSH Terms] field tags
          3. AND the sub-queries together (both terms must match)
          4. Post-fetch: enforce date range strictly

        Query strategy (use_raw_query=True):
          Pass the query directly to PubMed's esearch, matching the
          results you would get from PubMed's own web search.
        """
        self.last_corrected_query = None
        try:
            logger.info(f"Starting PubMed search for: {query}")
            logger.info(f"Parameters: max_results={max_results}, "
                        f"start_date={start_date}, end_date={end_date}, "
                        f"use_raw_query={use_raw_query}")

            search_query = self._build_search_query(
                query, start_date, end_date, use_raw_query
            )
            logger.info(f"Final PubMed query: {search_query}")

            df = self._fetch_papers(
                search_query, max_results, cancel_event, progress_callback=progress_callback
            )

            # ── Zero-result spell-check fallback ────────────────────────
            # PubMed's E-utilities (unlike the website) do not auto-correct
            # spelling, so a typo silently returns nothing. When the first
            # search comes back empty, ask ESpell for a corrected spelling
            # and retry once with it. Skip if the search was cancelled.
            if df.empty and not self._is_cancelled(cancel_event):
                corrected = self._spell_check(query)
                if corrected:
                    logger.info(f"Retrying search with corrected query: '{corrected}'")
                    retry_query = self._build_search_query(
                        corrected, start_date, end_date, use_raw_query
                    )
                    logger.info(f"Final PubMed query (corrected): {retry_query}")
                    df = self._fetch_papers(
                        retry_query, max_results, cancel_event, progress_callback=progress_callback
                    )
                    if not df.empty:
                        self.last_corrected_query = corrected

            if df.empty:
                logger.warning("No papers found for query")
                return pd.DataFrame()

            # ── Post-fetch date filter ──────────────────────────────────
            if start_date or end_date:
                years = pd.to_numeric(df['Publication Year'], errors='coerce')
                mask = pd.Series([True] * len(df))
                if start_date:
                    mask = mask & (years >= start_date.year)
                if end_date:
                    mask = mask & (years <= end_date.year)
                before = len(df)
                df = df[mask].reset_index(drop=True)
                logger.info(
                    f"Date filter: {before} -> {len(df)} papers "
                    f"within {getattr(start_date, 'year', '?')}-"
                    f"{getattr(end_date, 'year', '?')}"
                )

            # ── NO post-hoc score filtering ─────────────────────────────
            # Reason: PubMed's [MeSH Terms] field tagging is authoritative.
            # Papers that don't mention "smart healthcare" verbatim in their
            # title/abstract are still legitimately relevant if PubMed tagged
            # them with matching MeSH descriptors. Score filtering based on
            # keyword presence incorrectly removes these papers.
            # PubMed's own AND query between term blocks already enforces
            # that both topics are present — no further filtering needed.

            df = df.head(max_results).reset_index(drop=True)
            logger.info(f"Final result count: {len(df)} (target: {max_results})")
            return df

        except Exception as e:
            logger.error(f"Error in search_and_retrieve_optimized: {e}")
            return pd.DataFrame()

    # ------------------------------------------------------------------
    # PubMed API helpers
    # ------------------------------------------------------------------

    def _build_search_query(
        self,
        query: str,
        start_date: Optional[date],
        end_date: Optional[date],
        use_raw_query: bool,
    ) -> str:
        """Build the final PubMed `term` string for a given user query."""
        if use_raw_query:
            search_query = query.strip()
            logger.info("Using raw query mode — no expansion applied")
        else:
            terms = [t.strip() for t in query.split(",") if t.strip()]
            # Build AND query — each term must appear (in some form)
            if len(terms) > 1:
                term_blocks = [self._build_expanded_query_for_term(t) for t in terms]
                # AND between term blocks: paper must match ALL terms
                search_query = " AND ".join(term_blocks)
            else:
                search_query = self._build_expanded_query_for_term(query.strip())

        if start_date or end_date:
            date_filter = self._build_date_filter(start_date, end_date)
            search_query = f"({search_query}) AND {date_filter}"

        return search_query

    @staticmethod
    def _is_cancelled(cancel_event: Optional[Any]) -> bool:
        """True if a cancellation flag has been set by the caller."""
        return cancel_event is not None and cancel_event.is_set()

    def _fetch_papers(
        self,
        search_query: str,
        max_results: int,
        cancel_event: Optional[Any] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> pd.DataFrame:
        """Page through esearch/efetch for a built query and collect papers."""
        self._failed_pmids = []
        self._failed_batches_count = 0
        self.last_retrieval_report = {}

        # Page size for ESearch: up to 5000 per request
        esearch_page_size = min(max_results, 5000)

        # 1. First ESearch page
        first_pmids, total_count = self._esearch_pmids_and_count(
            search_query, esearch_page_size, 0
        )

        if not first_pmids or total_count == 0:
            logger.warning(f"No PMIDs found for query: {search_query}")
            self.last_retrieval_report = {
                "total_esearch_count": total_count,
                "pmids_retrieved": 0,
                "records_fetched": 0,
                "failed_pmids": [],
                "failed_batches_count": 0,
                "is_complete": True,
                "warning": None,
                "enrichment_warning": None,
            }
            return pd.DataFrame()

        target_count = min(max_results, total_count)
        logger.info(f"PubMed total count: {total_count}, requested target: {target_count}")

        all_pmids: List[str] = []
        seen_pmids: Set[str] = set()

        for p in first_pmids:
            if p not in seen_pmids:
                seen_pmids.add(p)
                all_pmids.append(p)

        if progress_callback:
            progress_callback({
                "phase": "esearch",
                "retrieved": len(all_pmids),
                "target": target_count,
                "total": total_count,
                "message": f"ESearch: collected {len(all_pmids)} of {target_count} PMIDs (total available: {total_count})",
            })

        # 2. Paginate ESearch if more PMIDs are needed
        current_offset = len(first_pmids)
        while len(all_pmids) < target_count and current_offset < total_count:
            if self._is_cancelled(cancel_event):
                logger.info("Search cancelled during PMID pagination — stopping fetch loop")
                break

            page_limit = min(target_count - len(all_pmids), 5000)
            logger.info(f"Paginating ESearch: fetching up to {page_limit} PMIDs at offset {current_offset}")

            next_pmids, _ = self._esearch_pmids_and_count(
                search_query, page_limit, current_offset
            )

            if not next_pmids:
                logger.info(f"No more PMIDs returned at offset {current_offset}")
                break

            new_count = 0
            for p in next_pmids:
                if p not in seen_pmids:
                    seen_pmids.add(p)
                    all_pmids.append(p)
                    new_count += 1
                    if len(all_pmids) >= target_count:
                        break

            current_offset += len(next_pmids)

            if progress_callback:
                progress_callback({
                    "phase": "esearch",
                    "retrieved": len(all_pmids),
                    "target": target_count,
                    "total": total_count,
                    "message": f"ESearch: collected {len(all_pmids)} of {target_count} PMIDs",
                })

            if new_count == 0 or len(next_pmids) < page_limit:
                break

        # Ensure exact slice up to target_count
        all_pmids = all_pmids[:target_count]
        logger.info(f"Total PMIDs collected for retrieval: {len(all_pmids)}")

        if self._is_cancelled(cancel_event):
            logger.info("Search cancelled before detail retrieval")
            return pd.DataFrame()

        if progress_callback:
            progress_callback({
                "phase": "efetch_start",
                "total_pmids": len(all_pmids),
                "message": f"Retrieved {len(all_pmids)} PMIDs; starting batch detail retrieval...",
            })

        # 3. Retrieve paper details in batches with retry and subdivision
        if progress_callback is not None:
            papers = self._retrieve_paper_details(
                all_pmids, cancel_event=cancel_event, progress_callback=progress_callback
            )
        else:
            papers = self._retrieve_paper_details(all_pmids, cancel_event=cancel_event)
        df = pd.DataFrame(papers) if papers else pd.DataFrame()

        # 4. Generate structured retrieval report
        warning_msg: Optional[str] = None
        if self._failed_pmids:
            num_failed = len(self._failed_pmids)
            pmid_sample = ", ".join(self._failed_pmids[:5])
            suffix = "..." if num_failed > 5 else ""
            warning_msg = (
                f"Retrieved {len(df)} of {target_count} records. "
                f"{num_failed} record(s) could not be retrieved from PubMed (PMID: {pmid_sample}{suffix})."
            )
        elif self.last_enrichment_warning:
            warning_msg = self.last_enrichment_warning

        self.last_retrieval_report = {
            "total_esearch_count": total_count,
            "pmids_retrieved": len(all_pmids),
            "records_fetched": len(df),
            "failed_pmids": list(self._failed_pmids),
            "failed_batches_count": self._failed_batches_count,
            "is_complete": (len(self._failed_pmids) == 0 and len(df) >= target_count),
            "warning": warning_msg,
            "enrichment_warning": self.last_enrichment_warning,
        }

        return df

    def _build_date_filter(
        self, start_date: Optional[date], end_date: Optional[date]
    ) -> str:
        if start_date and end_date:
            return (f"{start_date.strftime('%Y/%m/%d')}:"
                    f"{end_date.strftime('%Y/%m/%d')}[pdat]")
        elif start_date:
            return f"{start_date.strftime('%Y/%m/%d')}:3000/12/31[pdat]"
        elif end_date:
            return f"1900/01/01:{end_date.strftime('%Y/%m/%d')}[pdat]"
        return ""

    def _esearch_pmids_and_count(
        self, query: str, retmax: int, offset: int = 0
    ) -> Tuple[List[str], int]:
        """Search for PMIDs using esearch (POST) and return both PMIDs and total count."""
        try:
            data = {
                'db': 'pubmed',
                'term': query,
                'retmax': min(max(retmax, 0), 10000),
                'retstart': offset,
                'retmode': 'xml',
            }
            logger.info(f"esearch POST — retmax={data['retmax']}, retstart={offset}")
            response = self._post_with_retry('esearch.fcgi', data)

            root = ET.fromstring(response.content)

            # Extract total count
            count_elem = root.find('.//Count')
            total_count = int(count_elem.text.strip()) if count_elem is not None and count_elem.text else 0

            # Extract PMIDs in order
            pmids: List[str] = []
            id_list_elem = root.find('.//IdList')
            if id_list_elem is not None:
                for id_elem in id_list_elem.findall('Id'):
                    if id_elem.text and id_elem.text.strip():
                        pmids.append(id_elem.text.strip())
            else:
                for id_elem in root.findall('.//Id'):
                    if id_elem.text and id_elem.text.strip():
                        pmids.append(id_elem.text.strip())

            logger.info(f"esearch found {len(pmids)} PMIDs (total available: {total_count})")
            return pmids, total_count

        except Exception as e:
            logger.error(f"Error in _esearch_pmids_and_count: {e}")
            return [], 0

    def _search_pmids(self, query: str, max_results: int) -> List[str]:
        return self._search_pmids_with_offset(query, max_results, 0)

    def _search_pmids_with_offset(
        self, query: str, max_results: int, offset: int = 0
    ) -> List[str]:
        """Search for PMIDs using esearch (POST). Maintained for backward compatibility."""
        pmids, _ = self._esearch_pmids_and_count(query, max_results, offset)
        return pmids

    def _retrieve_paper_details(
        self,
        pmids: List[str],
        cancel_event: Optional[Any] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve paper details using efetch + esummary (POST), batch size 50 with retry/subdivision."""
        papers = []
        batch_size = 50
        total_batches = (len(pmids) + batch_size - 1) // batch_size

        for i in range(0, len(pmids), batch_size):
            if self._is_cancelled(cancel_event):
                logger.info("Detail retrieval cancelled")
                break

            batch_pmids = pmids[i:i + batch_size]
            batch_papers = self._fetch_batch_with_retry(batch_pmids, cancel_event=cancel_event)
            papers.extend(batch_papers)
            batch_num = i // batch_size + 1
            logger.info(
                f"Batch {batch_num}/{total_batches}: "
                f"{len(batch_papers)} papers (total {len(papers)})"
            )

            if progress_callback:
                progress_callback({
                    "phase": "efetch",
                    "batch": batch_num,
                    "total_batches": total_batches,
                    "records_fetched": len(papers),
                    "target": len(pmids),
                    "message": f"EFetch: batch {batch_num}/{total_batches} ({len(papers)} records fetched)",
                })

        return papers

    def _fetch_batch_with_retry(
        self,
        batch_pmids: List[str],
        cancel_event: Optional[Any] = None,
        max_batch_retries: int = 3,
        depth: int = 0,
        max_depth: int = 2,
    ) -> List[Dict[str, Any]]:
        """
        Fetch details for a batch of PMIDs with unified retry and bounded subdivision.
        Eliminates nested retry multiplication while preserving split-and-retry recovery.
        """
        if not batch_pmids or self._is_cancelled(cancel_event):
            return []

        last_err: Optional[Exception] = None
        # At depth 0, attempt max_batch_retries. At depth > 0 (subdivided sub-batch), attempt 1 retry.
        effective_retries = max_batch_retries if depth == 0 else 1

        for attempt in range(effective_retries):
            if self._is_cancelled(cancel_event):
                return []
            try:
                efetch_data = {
                    'db': 'pubmed',
                    'id': ','.join(batch_pmids),
                    'retmode': 'xml',
                }
                response = self._post_with_retry('efetch.fcgi', efetch_data)

                summary_details = {}
                try:
                    summary_details = self._fetch_summary_details(batch_pmids)
                except Exception as sum_err:
                    logger.warning(f"Error fetching summary for batch: {sum_err}; continuing with XML data")

                batch_papers = self._parse_pubmed_xml(response.content, summary_details)
                return batch_papers

            except Exception as e:
                last_err = e
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                logger.warning(
                    f"EFetch batch ({len(batch_pmids)} PMIDs, depth {depth}) attempt {attempt+1}/{effective_retries} failed: {e}. "
                    f"Retrying in {wait}s..."
                )
                time.sleep(wait)

        # Batch failed all retry attempts. Subdivide (split-and-retry) up to max_depth
        if len(batch_pmids) > 1 and depth < max_depth:
            mid = len(batch_pmids) // 2
            left_pmids = batch_pmids[:mid]
            right_pmids = batch_pmids[mid:]
            logger.warning(
                f"Batch of {len(batch_pmids)} failed after {effective_retries} attempts ({last_err}). "
                f"Subdividing into {len(left_pmids)} and {len(right_pmids)} PMIDs at depth {depth + 1}."
            )
            rescued_papers = []
            rescued_papers.extend(
                self._fetch_batch_with_retry(
                    left_pmids, cancel_event=cancel_event, max_batch_retries=1, depth=depth + 1, max_depth=max_depth
                )
            )
            rescued_papers.extend(
                self._fetch_batch_with_retry(
                    right_pmids, cancel_event=cancel_event, max_batch_retries=1, depth=depth + 1, max_depth=max_depth
                )
            )
            return rescued_papers
        else:
            for failed_id in batch_pmids:
                if failed_id not in self._failed_pmids:
                    self._failed_pmids.append(failed_id)
            self._failed_batches_count += 1
            logger.error(
                f"Permanently failed to fetch details for {len(batch_pmids)} PMID(s) ({batch_pmids}) at depth {depth}: {last_err}"
            )
            return []

    def _fetch_summary_details(
        self, pmids: List[str]
    ) -> Dict[str, Dict[str, str]]:
        """Fetch PubMed summary metadata via POST with bounded retry."""
        try:
            data = {
                'db': 'pubmed',
                'id': ','.join(pmids),
                'retmode': 'json',
            }
            response = self._post_with_retry('esummary.fcgi', data)
            payload = response.json()
            result = payload.get('result', {})
            summary_map: Dict[str, Dict[str, str]] = {}

            for pmid in result.get('uids', []):
                doc = result.get(str(pmid), {})
                summary_map[str(pmid)] = {
                    'publication_year': self._extract_year_from_text(
                        doc.get('pubdate', '')
                    ) or "",
                    'journal': doc.get('fulljournalname') or doc.get('source') or "",
                }
            return summary_map
        except Exception as e:
            logger.warning(f"Unable to fetch summary details: {e}")
            return {}

    def _parse_pubmed_xml(
        self,
        xml_content: bytes,
        summary_details: Optional[Dict[str, Dict[str, str]]] = None
    ) -> List[Dict[str, Any]]:
        papers = []
        summary_details = summary_details or {}
        try:
            root = ET.fromstring(xml_content)
            article_elems = [
                elem for elem in root.iter()
                if elem.tag in ('PubmedArticle', 'PubmedBookArticle')
            ]
            for elem in article_elems:
                if elem.tag == 'PubmedArticle':
                    try:
                        paper = self._extract_paper_info(elem, summary_details)
                        if paper:
                            papers.append(paper)
                    except Exception as e:
                        logger.warning(f"Error parsing article: {e}")
                elif elem.tag == 'PubmedBookArticle':
                    try:
                        paper = self._extract_book_info(elem, summary_details)
                        if paper:
                            papers.append(paper)
                    except Exception as e:
                        logger.warning(f"Error parsing book article: {e}")

            # Batch enrich PMC IDs for any papers missing PMCID in XML
            if papers:
                self._enrich_pmc_ids(papers)
        except Exception as e:
            logger.error(f"Error parsing XML: {e}")
        return papers

    def _enrich_pmc_ids(self, papers: List[Dict[str, Any]]) -> None:
        """
        Enrich papers missing PMCID using official NCBI PMC ID Converter API.
        Non-blocking: deduplicates queried PMIDs, uses a bounded timeout (4s),
        trips a circuit breaker on consecutive timeouts, preserves PubMed records,
        and reports enrichment warnings.
        """
        if self._pmc_circuit_broken or not papers:
            return

        missing_pmids = [
            str(p['PMID']).strip() for p in papers
            if p.get('PMID') and not p.get('PMCID') and str(p['PMID']).strip() not in self._pmc_attempted_pmids
        ]
        if not missing_pmids:
            return

        # Mark as attempted immediately so we never re-request the same PMIDs
        for pmid in missing_pmids:
            self._pmc_attempted_pmids.add(pmid)

        try:
            for i in range(0, len(missing_pmids), 100):
                if self._pmc_circuit_broken:
                    break
                chunk = missing_pmids[i:i + 100]
                url = (
                    f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
                    f"?ids={','.join(chunk)}&format=json&tool=ResearchRover&email={self.email}"
                )
                try:
                    time.sleep(self.rate_limit)
                    resp = self.session.get(url, timeout=4)
                    if resp.status_code == 200:
                        self._pmc_consecutive_failures = 0
                        data = resp.json()
                        for rec in data.get('records', []):
                            pmid = str(rec.get('pmid') or '').strip()
                            pmcid = rec.get('pmcid')
                            if pmid and pmcid:
                                clean_pmc = str(pmcid).strip()
                                if not clean_pmc.upper().startswith("PMC"):
                                    clean_pmc = f"PMC{clean_pmc}"
                                for p in papers:
                                    if str(p.get('PMID', '')).strip() == pmid:
                                        p['PMCID'] = clean_pmc
                                        p['pmcid'] = clean_pmc
                                        p['PDF_URL'] = f"https://pmc.ncbi.nlm.nih.gov/articles/{clean_pmc}/pdf/"
                                        p['pdf_url'] = p['PDF_URL']
                                        p['Is_OA'] = True
                                        p['is_oa'] = True
                                        break
                    else:
                        self._pmc_consecutive_failures += 1
                        logger.warning(f"PMC idconv returned HTTP {resp.status_code}")
                except Exception as req_err:
                    self._pmc_consecutive_failures += 1
                    logger.warning(f"Failed to batch-enrich PMC IDs via NCBI idconv: {req_err}")

                if self._pmc_consecutive_failures >= self.MAX_PMC_CONSECUTIVE_FAILURES:
                    self._pmc_circuit_broken = True
                    self.last_enrichment_warning = (
                        "PMC ID enrichment service temporarily unavailable (idconv timeout); "
                        "proceeding with standard PubMed metadata."
                    )
                    logger.warning(
                        f"PMC ID enrichment circuit breaker tripped after {self._pmc_consecutive_failures} consecutive failures. "
                        "Disabling further idconv calls for this search run."
                    )
                    break
        except Exception as e:
            logger.warning(f"Unexpected error in PMC enrichment: {e}")

    def _extract_paper_info(
        self,
        article,
        summary_details: Optional[Dict[str, Dict[str, str]]] = None
    ) -> Optional[Dict[str, Any]]:
        try:
            summary_details = summary_details or {}

            title_elem = article.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else "Unknown"
            if title:
                title = re.sub(r'<[^>]+>', '', str(title)).strip()

            abstract_elem = article.find('.//AbstractText')
            abstract = abstract_elem.text if abstract_elem is not None else ""
            if abstract:
                abstract = re.sub(r'<[^>]+>', '', str(abstract)).strip()

            doi = pmcid = nihms_id = ""
            for article_id in article.findall('.//ArticleId'):
                id_type = article_id.get('IdType')
                if id_type == 'doi' and not doi:
                    doi = article_id.text or ""
                elif id_type == 'pmc' and not pmcid:
                    pmcid = article_id.text or ""
                elif id_type == 'mid' and not nihms_id:
                    nihms_id = article_id.text or ""

            pmid_elem = article.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else ""
            summary = summary_details.get(pmid, {})

            journal_elem = article.find('.//Journal/Title')
            if journal_elem is None:
                journal_elem = article.find('.//Journal/ISOAbbreviation')
            journal = journal_elem.text if journal_elem is not None else "Unknown"
            journal = summary.get('journal') or journal
            publication_year = (
                summary.get('publication_year')
                or self._extract_publication_year(article)
            )
            create_date = self._extract_create_date(article)

            # --- FIX: read Authors list directly from parsed XML ---
            authors = []
            for author in article.findall('.//Author'):
                ln = author.find('LastName')
                fn = author.find('ForeName')
                initials = author.find('Initials')
                collective = author.find('CollectiveName')
                if collective is not None and collective.text:
                    authors.append(collective.text.strip())
                elif ln is not None and ln.text:
                    lastname = ln.text.strip()
                    # Use ForeName if available, else Initials
                    if fn is not None and fn.text:
                        firstname = fn.text.strip()
                    elif initials is not None and initials.text:
                        firstname = initials.text.strip()
                    else:
                        firstname = ""
                    full = f"{firstname} {lastname}".strip() if firstname else lastname
                    if full:
                        authors.append(full)
            first_author = authors[0] if authors else ""

            # Extract Author and Article Affiliations from XML
            affiliations = []
            for aff_elem in article.findall('.//AffiliationInfo/Affiliation'):
                if aff_elem is not None:
                    aff_text = "".join(aff_elem.itertext()).strip()
                    if aff_text and aff_text not in affiliations:
                        affiliations.append(aff_text)

            keywords = [
                kw.text.strip()
                for kw in article.findall('.//Keyword')
                if kw.text
            ]

            # Extract MeSH terms from the article XML
            mesh_terms = [
                mh.find('DescriptorName').text.strip()
                for mh in article.findall('.//MeshHeading')
                if mh.find('DescriptorName') is not None
                and mh.find('DescriptorName').text
            ]

            download_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""
            citation = self._build_citation(article, journal, publication_year, doi)
            reference = citation or f"{title}. {journal}. {publication_year}."

            clean_pmc = pmcid.strip() if pmcid else ""
            if clean_pmc and not clean_pmc.upper().startswith("PMC"):
                clean_pmc = f"PMC{clean_pmc}"

            pdf_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{clean_pmc}/pdf/" if clean_pmc else None
            is_oa = True if clean_pmc else False

            return {
                'Title':            title,
                'Abstract':         abstract,
                'Publication Year': publication_year,
                'Source':           journal,
                'Journal/Book':     journal,
                # Use 'DOI' consistently (search_service reads 'DOI' first, then 'Doi' as fallback)
                'DOI':              doi,
                'Download_URL':     download_url,
                'Keywords':         keywords,
                'MeSH_Terms':       mesh_terms,
                'Authors':          authors,
                'Affiliations':     affiliations,
                'PMID':             pmid,
                'Citation':         citation,
                'Create Date':      create_date,
                'PMCID':            clean_pmc or None,
                'pmcid':            clean_pmc or None,
                'PDF_URL':          pdf_url,
                'pdf_url':          pdf_url,
                'Is_OA':            is_oa,
                'is_oa':            is_oa,
                'NIHMS ID':         nihms_id,
                'First Author':     first_author,
                'Reference':        reference,
            }

        except Exception as e:
            logger.error(f"Error extracting paper info: {e}")
            return None

    def _extract_publication_year(self, article) -> str:
        pub_date = article.find('.//JournalIssue/PubDate')
        year = self._extract_year_from_pubdate(pub_date)
        if year:
            return year
        article_date = article.find(".//ArticleDate[@DateType='Electronic']")
        year = self._extract_year_from_pubdate(article_date)
        if year:
            return year
        medline_date = article.find('.//MedlineDate')
        if medline_date is not None and medline_date.text:
            year = self._extract_year_from_text(medline_date.text)
            if year:
                return year
        return "Unknown"

    def _extract_create_date(self, article) -> str:
        pubmed_data = article.find('.//PubmedData/History')
        if pubmed_data is None:
            pubmed_data = article.find('.//PubmedBookData/History')
        if pubmed_data is None:
            return ""
        for pubmed_date in pubmed_data.findall(
            "PubMedPubDate[@PubStatus='pubmed']"
        ):
            date_str = self._format_pubmed_date(pubmed_date)
            if date_str:
                return date_str
        first_date = pubmed_data.find('PubMedPubDate')
        return self._format_pubmed_date(first_date) if first_date is not None else ""

    def _extract_book_info(
        self,
        book_article,
        summary_details: Optional[Dict[str, Dict[str, str]]] = None
    ) -> Optional[Dict[str, Any]]:
        """Extract canonical paper dictionary from a PubmedBookArticle XML element."""
        try:
            summary_details = summary_details or {}

            # 1. Title: Chapter title first (ArticleTitle), fallback to BookTitle
            title_elem = book_article.find('.//ArticleTitle')
            if title_elem is None or not title_elem.text:
                title_elem = book_article.find('.//Book/BookTitle')
            if title_elem is None or not title_elem.text:
                title_elem = book_article.find('.//BookTitle')
            title = title_elem.text if title_elem is not None else "Unknown"
            if title:
                title = re.sub(r'<[^>]+>', '', str(title)).strip()

            # 2. Abstract: Can have multiple AbstractText elements
            abstract_parts = []
            for ab_elem in book_article.findall('.//AbstractText'):
                label = ab_elem.get('Label')
                ab_text = "".join(ab_elem.itertext()).strip()
                if ab_text:
                    if label:
                        abstract_parts.append(f"{label}: {ab_text}")
                    else:
                        abstract_parts.append(ab_text)
            abstract = "\n\n".join(abstract_parts) if abstract_parts else ""
            if abstract:
                abstract = re.sub(r'<[^>]+>', '', abstract).strip()

            # 3. Identifiers
            doi = pmcid = nihms_id = book_accession = ""
            for article_id in book_article.findall('.//ArticleId'):
                id_type = article_id.get('IdType')
                if id_type == 'doi' and not doi:
                    doi = article_id.text or ""
                elif id_type == 'pmc' and not pmcid:
                    pmcid = article_id.text or ""
                elif id_type == 'mid' and not nihms_id:
                    nihms_id = article_id.text or ""
                elif id_type == 'bookaccession' and not book_accession:
                    book_accession = article_id.text or ""

            pmid_elem = book_article.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else ""
            if not pmid:
                for article_id in book_article.findall('.//ArticleId'):
                    if article_id.get('IdType') == 'pubmed' and article_id.text:
                        pmid = article_id.text
                        break

            summary = summary_details.get(pmid, {})

            # 4. Book Title and Publisher
            book_title_elem = book_article.find('.//Book/BookTitle')
            if book_title_elem is None:
                book_title_elem = book_article.find('.//BookTitle')
            book_title = "".join(book_title_elem.itertext()).strip() if book_title_elem is not None else ""
            if not book_title:
                book_title = summary.get('journal') or "NCBI Bookshelf"

            pub_name_elem = book_article.find('.//Book/Publisher/PublisherName')
            if pub_name_elem is None:
                pub_name_elem = book_article.find('.//Publisher/PublisherName')
            publisher = pub_name_elem.text.strip() if pub_name_elem is not None and pub_name_elem.text else ""

            journal = book_title

            # 5. Publication Year
            publication_year = summary.get('publication_year') or ""
            if not publication_year:
                contrib_date = book_article.find('.//ContributionDate')
                publication_year = self._extract_year_from_pubdate(contrib_date) or ""
            if not publication_year:
                book_date = book_article.find('.//Book/PubDate')
                publication_year = self._extract_year_from_pubdate(book_date) or ""
            if not publication_year:
                create_dt = self._extract_create_date(book_article)
                publication_year = self._extract_year_from_text(create_dt) or "Unknown"

            create_date = self._extract_create_date(book_article)

            # 6. Authors
            authors = []
            author_lists = book_article.findall(".//BookDocument/AuthorList[@Type='authors']")
            if not author_lists:
                author_lists = book_article.findall(".//AuthorList[@Type='authors']")
            if not author_lists:
                author_lists = book_article.findall(".//BookDocument/AuthorList")
            if not author_lists:
                author_lists = book_article.findall(".//Book/AuthorList")

            for al in author_lists:
                for author in al.findall('Author'):
                    ln = author.find('LastName')
                    fn = author.find('ForeName')
                    initials = author.find('Initials')
                    collective = author.find('CollectiveName')
                    if collective is not None and collective.text:
                        authors.append(collective.text.strip())
                    elif ln is not None and ln.text:
                        lastname = ln.text.strip()
                        if fn is not None and fn.text:
                            firstname = fn.text.strip()
                        elif initials is not None and initials.text:
                            firstname = initials.text.strip()
                        else:
                            firstname = ""
                        full = f"{firstname} {lastname}".strip() if firstname else lastname
                        if full and full not in authors:
                            authors.append(full)
                if authors:
                    break

            first_author = authors[0] if authors else ""

            # 7. Affiliations
            affiliations = []
            for aff_elem in book_article.findall('.//AffiliationInfo/Affiliation'):
                if aff_elem is not None:
                    aff_text = "".join(aff_elem.itertext()).strip()
                    if aff_text and aff_text not in affiliations:
                        affiliations.append(aff_text)

            # 8. Keywords
            keywords = [
                kw.text.strip()
                for kw in book_article.findall('.//Keyword')
                if kw.text
            ]

            # 9. MeSH / Sections
            mesh_terms = [
                mh.find('DescriptorName').text.strip()
                for mh in book_article.findall('.//MeshHeading')
                if mh.find('DescriptorName') is not None and mh.find('DescriptorName').text
            ]

            # 10. Citation
            citation = self._build_book_citation(
                book_article, book_title, publisher, publication_year, doi
            )
            reference = citation or f"{title}. In: {book_title}. {publication_year}."

            clean_pmc = pmcid.strip() if pmcid else ""
            if clean_pmc and not clean_pmc.upper().startswith("PMC"):
                clean_pmc = f"PMC{clean_pmc}"

            pdf_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{clean_pmc}/pdf/" if clean_pmc else None
            is_oa = True if clean_pmc else False
            download_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""

            return {
                'Title':            title,
                'Abstract':         abstract,
                'Publication Year': publication_year,
                'Source':           journal,
                'Journal/Book':     journal,
                'DOI':              doi,
                'Download_URL':     download_url,
                'Keywords':         keywords,
                'MeSH_Terms':       mesh_terms,
                'Authors':          authors,
                'Affiliations':     affiliations,
                'PMID':             pmid,
                'Citation':         citation,
                'Create Date':      create_date,
                'PMCID':            clean_pmc or None,
                'pmcid':            clean_pmc or None,
                'PDF_URL':          pdf_url,
                'pdf_url':          pdf_url,
                'Is_OA':            is_oa,
                'is_oa':            is_oa,
                'NIHMS ID':         nihms_id,
                'First Author':     first_author,
                'Reference':        reference,
            }
        except Exception as e:
            logger.error(f"Error extracting book info: {e}")
            return None

    def _build_book_citation(
        self, book_article, book_title: str, publisher: str, publication_year: str, doi: str
    ) -> str:
        parts = []
        if book_title:
            parts.append(f"In: {book_title}")
        if publisher:
            parts.append(publisher)
        if publication_year and publication_year != "Unknown":
            parts.append(publication_year)

        citation = ". ".join(p for p in parts if p).strip()
        if citation and not citation.endswith('.'):
            citation += '.'
        if doi:
            citation = f"{citation} doi: {doi}".strip()
            if not citation.endswith('.'):
                citation += '.'
        return citation

    def _build_citation(
        self, article, journal: str, publication_year: str, doi: str
    ) -> str:
        citation_parts = []
        if journal and journal != "Unknown":
            citation_parts.append(journal)

        pub_date = article.find('.//JournalIssue/PubDate')
        medline_date = ""
        if pub_date is not None:
            ml = pub_date.find('MedlineDate')
            if ml is not None and ml.text:
                medline_date = ml.text.strip()

        if medline_date:
            citation_parts.append(medline_date)
        elif publication_year and publication_year != "Unknown":
            month = self._get_text(pub_date, 'Month') if pub_date is not None else ""
            day   = self._get_text(pub_date, 'Day')   if pub_date is not None else ""
            frag  = publication_year
            if month:
                frag = f"{frag} {month}"
            if day:
                frag = f"{frag} {day}"
            citation_parts.append(frag)

        volume = self._get_text(article, './/JournalIssue/Volume')
        issue  = self._get_text(article, './/JournalIssue/Issue')
        pages  = self._get_text(article, './/Pagination/MedlinePgn')
        ids = []
        if volume:
            ids.append(f"{volume}({issue})" if issue else volume)
        elif issue:
            ids.append(f"({issue})")
        if pages:
            ids.append(pages)
        if ids:
            citation_parts.append(':'.join(ids) if len(ids) > 1 else ids[0])

        citation = '. '.join(p for p in citation_parts if p).strip()
        if citation and not citation.endswith('.'):
            citation += '.'
        if doi:
            citation = f"{citation} doi: {doi}".strip()
            if not citation.endswith('.'):
                citation += '.'
        return citation

    def _extract_year_from_pubdate(self, pub_date) -> Optional[str]:
        if pub_date is None:
            return None
        year_elem = pub_date.find('Year')
        if year_elem is not None and year_elem.text:
            return year_elem.text.strip()
        ml = pub_date.find('MedlineDate')
        if ml is not None and ml.text:
            return self._extract_year_from_text(ml.text)
        return None

    def _extract_year_from_text(self, text: str) -> Optional[str]:
        m = re.search(r'\b(19|20)\d{2}\b', text or "")
        return m.group() if m else None

    def _format_pubmed_date(self, date_elem) -> str:
        if date_elem is None:
            return ""
        year  = self._get_text(date_elem, 'Year')
        month = self._normalize_month(self._get_text(date_elem, 'Month'))
        day   = self._get_text(date_elem, 'Day')
        if not year:
            return ""
        month = month or "01"
        day   = day.zfill(2) if day else "01"
        return f"{day}-{month}-{year}"

    def _normalize_month(self, month: str) -> str:
        if not month:
            return ""
        month = month.strip()
        if month.isdigit():
            return month.zfill(2)
        month_map = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12',
        }
        return month_map.get(month[:3].lower(), "")

    def _get_text(self, element, path: str) -> str:
        if element is None:
            return ""
        child = element.find(path)
        if child is None or child.text is None:
            return ""
        return child.text.strip()


# Legacy alias for backward compatibility
OptimizedPubMedSearcher = PubMedService