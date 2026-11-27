"""
Search service for handling paper searches
"""

import asyncio
import csv
import json
import os
import sys
import re
from datetime import date
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Dict, Any, Callable, Tuple
import logging
import pandas as pd

from app.models.schemas import Paper, SearchSource
from app.core.config import Settings
from app.utils.csv_loader import read_csv_to_records, CSVLoadError, resolve_unique_csv_filename

from app.services.pubmed_service import PubMedService
from app.services.unified_search_service import UnifiedSearchService
from app.core.dependencies import get_reranker

logger = logging.getLogger("research_rover")

# Dedicated executor so PubMed's blocking sleep() calls don't exhaust
# the default thread pool and hang the server under concurrent requests
_pubmed_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="pubmed")


class SearchService:
    """Service for handling research paper searches"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.unified_service = UnifiedSearchService(settings)
        # Set after a PubMed search if ESpell corrected the query and the
        # corrected spelling produced the results. None otherwise.
        self.last_corrected_query: Optional[str] = None
        self.last_warning: Optional[str] = None
        self.last_total_esearch_count: Optional[int] = None
        self.last_retrieval_report: Optional[Dict[str, Any]] = None

    def _improve_pubmed_query(self, query: str) -> str:
        """
        Lightly normalise the query for PubMed.
        Only expands well-known abbreviations; does NOT lowercase the whole
        query (PubMed is case-insensitive anyway) and does NOT strip stop
        words (they can be meaningful inside quoted phrases).
        """
        abbreviations = {
            'ml':  'machine learning',
            'ai':  'artificial intelligence',
            'dl':  'deep learning',
            'nlp': 'natural language processing',
            'cv':  'computer vision',
            'iot': 'internet of things',
            'ehr': 'electronic health records',
            'emr': 'electronic medical records',
        }

        improved = query
        for abbrev, full_term in abbreviations.items():
            # Word-boundary replacement, case-insensitive
            pattern = r'(?<![a-zA-Z])' + re.escape(abbrev) + r'(?![a-zA-Z])'
            improved = re.sub(pattern, full_term, improved, flags=re.IGNORECASE)

        if len(improved.strip()) < 3:
            return query
        return improved

    async def search_papers(
        self,
        query: str,
        max_results: int = 10,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        search_source: SearchSource = SearchSource.UNIFIED,
        use_raw_query: bool = False,
        cancel_event: Optional[Any] = None,
        sort_mode: str = "relevance",
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for papers using Unified Search (default), PubMed, or OpenAlex."""
        try:
            async def _fetch_pubmed(q, max_res, start_d, end_d, raw_q, cancel_ev):
                return await self._search_pubmed(
                    q, max_res, start_d, end_d, raw_q, cancel_ev, sort_mode, progress_callback=progress_callback
                )

            results = await self.unified_service.execute_search(
                query=query,
                max_results=max_results,
                start_date=start_date,
                end_date=end_date,
                search_source=search_source,
                use_raw_query=use_raw_query,
                cancel_event=cancel_event,
                pubmed_fetch_fn=_fetch_pubmed,
            )
            if self.unified_service.last_warning:
                self.last_warning = self.unified_service.last_warning
            return results
        except Exception as e:
            logger.error(f"Error in search_papers: {e}")
            raise

    async def _search_core(
        self,
        query: str,
        max_results: int,
        start_date: Optional[date],
        end_date: Optional[date]
    ) -> List[Dict[str, Any]]:
        logger.warning("CORE search not implemented yet, returning empty results")
        return []

    async def _search_pubmed(
        self,
        query: str,
        max_results: int,
        start_date: Optional[date],
        end_date: Optional[date],
        use_raw_query: bool = False,
        cancel_event: Optional[Any] = None,
        sort_mode: str = "relevance",
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> List[Dict[str, Any]]:
        """Search using PubMed API"""
        try:
            email   = self.settings.EMAIL or 'user@example.com'
            api_key = self.settings.PUBMED_API_KEY

            # Only apply abbreviation expansion when not in raw mode
            improved_query = query if use_raw_query else self._improve_pubmed_query(query)

            logger.info(f"PubMed search - Email: {email}")
            logger.info(f"PubMed search - API key present: {bool(api_key)}")
            logger.info(f"PubMed search - Original query: {query}")
            logger.info(f"PubMed search - Improved query: {improved_query}")
            logger.info(f"PubMed search - Max results: {max_results}")
            logger.info(f"PubMed search - Date range: {start_date}-{end_date}")
            logger.info(f"PubMed search - Raw query mode: {use_raw_query}")

            if not api_key:
                logger.error("PubMed API key not found in settings")
                return []

            loop = asyncio.get_event_loop()
            self.last_corrected_query = None

            def run_pubmed_search():
                searcher = PubMedService(email=email, api_key=api_key)
                df = searcher.search_and_retrieve_optimized(
                    query=improved_query,
                    start_date=start_date,
                    end_date=end_date,
                    max_results=max_results,
                    use_raw_query=use_raw_query,
                    cancel_event=cancel_event,
                    progress_callback=progress_callback,
                )
                report = getattr(searcher, 'last_retrieval_report', {}) or {}
                return df.to_dict('records'), searcher.last_corrected_query, report

            # Use dedicated executor to avoid blocking the default pool
            results, corrected, report = await loop.run_in_executor(
                _pubmed_executor, run_pubmed_search
            )
            self.last_corrected_query = corrected
            self.last_retrieval_report = report
            self.last_warning = report.get('warning')
            self.last_total_esearch_count = report.get('total_esearch_count')
            results = results or []

            # ── Second-stage ordering ───────────────────────────────────
            # PubMed returns candidates in chronological order. Re-order here:
            #   relevance → MedCPT semantic re-rank against the user's query
            #   recency   → explicit newest-first (already PubMed's order)
            # Re-ranking is CPU-bound, so run it off the event loop.
            if results and not self._is_cancelled(cancel_event):
                # Use the original user query for semantic intent, falling back
                # to the spelling-corrected query if that's what produced hits.
                rank_query = corrected or query
                results = await loop.run_in_executor(
                    _pubmed_executor, self._order_results, results, rank_query, sort_mode, progress_callback
                )

            return results

        except Exception as e:
            logger.error(f"Unexpected error during PubMed search: {e}")
            return []

    @staticmethod
    def _is_cancelled(cancel_event: Optional[Any]) -> bool:
        """True if the caller has signalled cancellation."""
        return cancel_event is not None and cancel_event.is_set()

    def _order_results(
        self,
        results: List[Dict[str, Any]],
        query: str,
        sort_mode: str,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Apply second-stage ordering to PubMed's candidate set.

        relevance → MedCPT semantic re-rank (attaches Relevance_Score/Rank).
        recency   → newest-first by publication year.
        Runs in a worker thread (CPU-bound). Fails open to PubMed order.
        """
        try:
            if sort_mode == "recency":
                from app.services.reranker_service import MedCPTReRanker
                return MedCPTReRanker.sort_by_recency(results)

            reranker = get_reranker()
            if reranker is None:
                return results
            return reranker.rerank(query, results, progress_callback=progress_callback)
        except Exception as e:
            logger.warning(f"Result ordering failed ({e}); using PubMed order.")
            return results

    async def save_results_to_csv(
        self,
        results: List[Dict[str, Any]],
        csv_path: str,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> Tuple[List[Paper], str]:
        """Save search results to CSV avoiding collisions and return processed papers with actual saved path"""
        try:
            if not results:
                return [], csv_path

            directory = os.path.dirname(os.path.abspath(csv_path)) if csv_path else (
                self.settings.DATA_FOLDER if hasattr(self, 'settings') and self.settings else 'data'
            )
            os.makedirs(directory, exist_ok=True)
            desired_filename = os.path.basename(csv_path) if csv_path else "search_results.csv"
            unique_filename = resolve_unique_csv_filename(directory, desired_filename)
            target_path = os.path.join(directory, unique_filename)

            if progress_callback:
                progress_callback({
                    "phase": "save",
                    "message": f"Saving {len(results)} papers to CSV: {unique_filename}",
                })

            logger.info(f"Converting {len(results)} results to DataFrame")
            df = pd.DataFrame(results)

            required_columns = ['Title', 'DOI', 'PMID', 'OpenAlex_ID', 'Abstract', 'Source', 'Download_URL',
                                 'Publication Year', 'Reference', 'Affiliations', 'Citation_Count', 'Is_OA', 'PDF_URL']
            for col in required_columns:
                if col not in df.columns:
                    if col == 'Title':
                        df[col] = 'Unknown Title'
                    elif col == 'Reference':
                        df[col] = df.apply(
                            lambda row: (
                                f"{row.get('Title','Unknown')}. "
                                f"{row.get('Source','Unknown Journal')}. "
                                f"{row.get('Publication Year','Unknown Year')}."
                            ), axis=1
                        )
                    else:
                        df[col] = ""

            def format_affiliations(val):
                if isinstance(val, list):
                    return "; ".join([str(v).strip() for v in val if str(v).strip()])
                if isinstance(val, str):
                    return val.strip()
                return ""

            if 'Affiliations' in df.columns:
                df['Affiliations'] = df['Affiliations'].apply(format_affiliations)

            logger.info(f"DataFrame shape: {df.shape}")
            df.to_csv(target_path, index=False, encoding='utf-8-sig')
            logger.info(f"CSV saved to {target_path}")

            self.last_saved_csv_path = target_path
            self.last_saved_csv_filename = unique_filename

            papers = []
            for result in results:
                try:
                    # Authors
                    authors = result.get('Authors', result.get('authors', []))
                    if isinstance(authors, str):
                        try:
                            import ast
                            authors = ast.literal_eval(authors)
                        except Exception:
                            authors = [a.strip() for a in authors.split(';') if a.strip()]
                    if not isinstance(authors, list):
                        authors = []

                    # Keywords
                    kw_raw = result.get('Keywords', result.get('keywords', []))
                    if isinstance(kw_raw, str):
                        try:
                            import ast
                            keywords = ast.literal_eval(kw_raw)
                        except Exception:
                            if ';' in kw_raw:
                                keywords = [k.strip() for k in kw_raw.split(';') if k.strip()]
                            else:
                                keywords = [k.strip() for k in kw_raw.split(',') if k.strip()]
                    elif isinstance(kw_raw, list):
                        keywords = kw_raw
                    else:
                        keywords = []

                    # Countries
                    c_raw = result.get('Countries', result.get('countries', []))
                    if isinstance(c_raw, str):
                        try:
                            import ast
                            countries = ast.literal_eval(c_raw)
                        except Exception:
                            countries = [c.strip() for c in c_raw.split(';') if c.strip()]
                    elif isinstance(c_raw, list):
                        countries = c_raw
                    else:
                        countries = []

                    source = str(result.get('Source', result.get('source', 'Unknown'))).strip() or 'Unknown'
                    title  = str(result.get('Title', result.get('title', 'Unknown'))).strip() or 'Unknown'

                    doi = str(result.get('DOI', '') or result.get('doi', '') or '').strip()
                    pmid = str(result.get('PMID', '') or result.get('pmid', '') or '').strip()
                    openalex_id = str(result.get('OpenAlex_ID', '') or result.get('openalex_id', '') or '').strip()

                    citation_count = result.get('Citation_Count', result.get('citation_count'))
                    if citation_count is not None:
                        try:
                            citation_count = int(citation_count)
                        except (ValueError, TypeError):
                            citation_count = None

                    is_oa = result.get('Is_OA', result.get('is_oa'))
                    if is_oa is not None and not isinstance(is_oa, bool):
                        if str(is_oa).lower() in ('true', '1'):
                            is_oa = True
                        elif str(is_oa).lower() in ('false', '0'):
                            is_oa = False
                        else:
                            is_oa = None

                    pdf_url = str(result.get('PDF_URL', '') or result.get('pdf_url', '') or '').strip() or None

                    paper = Paper(
                        source=source,
                        title=title,
                        download_url=result.get('Download_URL', result.get('download_url', '')),
                        year=str(result.get('Publication Year', result.get('Year_Published', result.get('year', 'Unknown')))),
                        keywords=keywords,
                        doi=doi,
                        pmid=pmid if pmid else None,
                        openalex_id=openalex_id if openalex_id else None,
                        authors=authors,
                        affiliations=result.get('Affiliations', result.get('affiliations')),
                        countries=countries,
                        abstract=result.get('Abstract', result.get('abstract', '')),
                        citation_count=citation_count,
                        is_oa=is_oa,
                        pdf_url=pdf_url,
                        relevance_score=result.get('Relevance_Score', result.get('relevance_score')),
                        relevance_rank=result.get('Relevance_Rank', result.get('relevance_rank')),
                    )
                    papers.append(paper)

                except Exception as e:
                    logger.warning(f"Error processing paper, using fallback: {e}")
                    try:
                        fallback = Paper(
                            source=str(result.get('Source', 'Unknown')).strip() or 'Unknown',
                            title=str(result.get('Title',  'Unknown')).strip() or 'Unknown',
                            download_url=str(result.get('Download_URL', '')).strip(),
                            year=str(result.get('Publication Year', result.get('Year_Published', 'Unknown'))).strip() or 'Unknown',
                            keywords=[],
                            doi=str(result.get('DOI', '') or result.get('Doi', '')).strip(),
                            authors=[],
                            abstract=str(result.get('Abstract', '')).strip()
                        )
                        papers.append(fallback)
                    except Exception as fe:
                        logger.error(f"Fallback also failed: {fe} — skipping paper")
                        continue

            logger.info(f"Paper processing: {len(results)} -> {len(papers)} papers")
            return papers, target_path

        except Exception as e:
            logger.error(f"Error saving results to CSV: {e}")
            raise

    async def load_papers_from_csv(self, csv_path: str, exclude_duplicates: bool = False) -> List[Paper]:
        """
        Load papers from CSV file using canonical loader with fallback.
        By default exclude_duplicates=False so the complete user catalogue is displayed.
        """
        papers = []
        try:
            from app.services.canonical_loader import CanonicalDataLoader
            canonical_records = CanonicalDataLoader.load_canonical_records(
                csv_path, exclude_duplicates=exclude_duplicates
            )
            for rec in canonical_records:
                try:
                    paper = Paper(
                        source=rec.journal or 'Unknown',
                        title=rec.title,
                        download_url=rec.download_url or '',
                        year=str(rec.publication_year) if rec.publication_year else 'Unknown',
                        keywords=rec.keywords,
                        doi=rec.doi or '',
                        pmid=rec.pmid,
                        openalex_id=rec.openalex_id,
                        authors=rec.authors,
                        affiliations="; ".join(rec.affiliations) if rec.affiliations else None,
                        countries=rec.countries,
                        abstract=rec.abstract or '',
                        citation_count=rec.citation_count,
                        is_oa=rec.is_open_access,
                        pdf_url=rec.url,
                    )
                    papers.append(paper)
                except Exception as e:
                    logger.warning(f"Error mapping canonical record to Paper: {e}")
                    continue
            if papers:
                return papers
        except Exception as e:
            logger.warning(f"Canonical loader fallback in SearchService: {e}")

        # Fallback to direct CSV row parsing for backward compatibility
        try:
            records = read_csv_to_records(csv_path)
            for row in records:
                try:
                    citation_count = row.get('Citation_Count') or row.get('citation_count')
                    if citation_count is not None and str(citation_count).strip():
                        try:
                            citation_count = int(citation_count)
                        except (ValueError, TypeError):
                            citation_count = None
                    else:
                        citation_count = None

                    is_oa_raw = row.get('Is_OA') or row.get('is_oa')
                    if is_oa_raw is not None and str(is_oa_raw).strip():
                        is_oa = str(is_oa_raw).lower() in ('true', '1')
                    else:
                        is_oa = None

                    paper = Paper(
                        source=str(row.get('Source', '')).strip() or 'Unknown',
                        title=str(row.get('Title', '')).strip() or 'Unknown',
                        download_url=str(row.get('Download_URL', '')).strip() or '',
                        year=str(row.get('Publication Year', row.get('Year_Published', ''))).strip() or 'Unknown',
                        keywords=self._process_keywords(row.get('Keywords', '')),
                        doi=str(row.get('DOI', '') or row.get('Doi', '')).strip() or '',
                        pmid=str(row.get('PMID', '') or row.get('pmid', '')).strip() or None,
                        openalex_id=str(row.get('OpenAlex_ID', '') or row.get('openalex_id', '')).strip() or None,
                        authors=self._process_authors(row.get('Authors', '')),
                        affiliations=str(row.get('Affiliations', '')).strip() or None,
                        countries=self._process_keywords(row.get('Countries', '')),
                        abstract=str(row.get('Abstract', '')).strip() or '',
                        citation_count=citation_count,
                        is_oa=is_oa,
                        pdf_url=str(row.get('PDF_URL', '') or row.get('pdf_url', '')).strip() or None,
                    )
                    papers.append(paper)
                except Exception as e:
                    logger.warning(f"Error processing CSV row: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error reading CSV file {csv_path}: {e}")
            raise
        return papers

    def _process_keywords(self, keyword_value: Any) -> List[str]:
        if isinstance(keyword_value, list):
            return keyword_value
        elif isinstance(keyword_value, str):
            kw = keyword_value.strip()
            if not kw:
                return []
            if kw.startswith('[') and kw.endswith(']'):
                try:
                    return json.loads(kw.replace("'", '"'))
                except Exception:
                    return [k.strip() for k in kw.strip('[]').split(',') if k.strip()]
            return [k.strip() for k in kw.split(',') if k.strip()]
        return []

    def _process_authors(self, authors_value: Any) -> List[str]:
        if isinstance(authors_value, list):
            return authors_value
        elif isinstance(authors_value, str):
            s = authors_value.strip()
            if not s:
                return []
            for sep in [';', ',', '|']:
                if sep in s:
                    return [a.strip() for a in s.split(sep) if a.strip()]
            return [s]
        return []