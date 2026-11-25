"""
Unit tests for PubMedService pagination, error recovery, and XML parsing in Research Rover.
All tests use mocked Entrez/E-utilities HTTP responses (no live network calls).
"""

import unittest
import os
import sys
import requests
from unittest.mock import MagicMock, patch
import pandas as pd
from xml.etree import ElementTree as ET

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.pubmed_service import PubMedService
from app.services.reranker_service import MedCPTReRanker
from app.core.config import Settings
from app.models.schemas import SearchSource
from app.services.search_service import SearchService


# ---------------------------------------------------------------------------
# Sample XML fixtures
# ---------------------------------------------------------------------------

SAMPLE_PUBMED_ARTICLE_XML = """
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation Status="MEDLINE">
      <PMID>38000001</PMID>
      <Article>
        <Journal>
          <JournalIssue>
            <PubDate><Year>2023</Year><Month>Nov</Month><Day>15</Day></PubDate>
          </JournalIssue>
          <Title>Journal of Medical Internet Research</Title>
        </Journal>
        <ArticleTitle>Screen Time and Adolescent Mental Health</ArticleTitle>
        <Abstract>
          <AbstractText>We investigated the association between screen time and mental health outcomes.</AbstractText>
        </Abstract>
        <AuthorList>
          <Author><LastName>Smith</LastName><ForeName>Alice</ForeName><Initials>A</Initials></Author>
          <Author><LastName>Johnson</LastName><ForeName>Bob</ForeName><Initials>B</Initials></Author>
        </AuthorList>
      </Article>
    </MedlineCitation>
    <PubmedData>
      <ArticleIdList>
        <ArticleId IdType="pubmed">38000001</ArticleId>
        <ArticleId IdType="doi">10.2196/12345</ArticleId>
        <ArticleId IdType="pmc">PMC1000001</ArticleId>
      </ArticleIdList>
    </PubmedData>
  </PubmedArticle>
</PubmedArticleSet>
"""

SAMPLE_BOOK_ARTICLE_XML = """
<PubmedArticleSet>
  <PubmedBookArticle>
    <BookDocument>
      <PMID>38000002</PMID>
      <ArticleIdList>
        <ArticleId IdType="pubmed">38000002</ArticleId>
        <ArticleId IdType="doi">10.1234/NBK54321.ch1</ArticleId>
        <ArticleId IdType="bookaccession">NBK54321</ArticleId>
        <ArticleId IdType="pmc">PMC1000002</ArticleId>
      </ArticleIdList>
      <Book>
        <Publisher>
          <PublisherName>National Academies Press (US)</PublisherName>
          <PublisherLocation>Washington (DC)</PublisherLocation>
        </Publisher>
        <BookTitle>Digital Media and Child Well-Being</BookTitle>
        <PubDate><Year>2022</Year></PubDate>
        <AuthorList Type="editors">
          <Author><LastName>Davis</LastName><ForeName>Carol</ForeName></Author>
        </AuthorList>
      </Book>
      <ArticleTitle>Chapter 1: Patterns of Screen Exposure in Early Childhood</ArticleTitle>
      <Abstract>
        <AbstractText Label="BACKGROUND">Digital screen exposure begins infancy.</AbstractText>
        <AbstractText Label="CONCLUSIONS">Caregivers should balance educational and recreational media.</AbstractText>
      </Abstract>
      <AuthorList Type="authors">
        <Author><LastName>Williams</LastName><ForeName>David</ForeName></Author>
      </AuthorList>
      <ContributionDate><Year>2022</Year></ContributionDate>
    </BookDocument>
    <PubmedBookData>
      <History>
        <PubMedPubDate PubStatus="pubmed">
          <Year>2022</Year><Month>5</Month><Day>20</Day>
        </PubMedPubDate>
      </History>
    </PubmedBookData>
  </PubmedBookArticle>
</PubmedArticleSet>
"""

SAMPLE_MIXED_ARTICLES_XML = f"""
<PubmedArticleSet>
{SAMPLE_PUBMED_ARTICLE_XML.split('<PubmedArticleSet>')[1].split('</PubmedArticleSet>')[0]}
{SAMPLE_BOOK_ARTICLE_XML.split('<PubmedArticleSet>')[1].split('</PubmedArticleSet>')[0]}
</PubmedArticleSet>
"""


class TestPubMedServicePagination(unittest.TestCase):
    """Test ESearch pagination beyond the old 3,000 cap and handling boundary limits."""

    def setUp(self):
        self.service = PubMedService(email="test@example.com", api_key="dummy_api_key")

    @patch.object(PubMedService, "_post_with_retry")
    def test_esearch_pmids_and_count(self, mock_post):
        """Verify _esearch_pmids_and_count parses both total <Count> and <IdList> correctly."""
        xml_resp = """<eSearchResult>
            <Count>7746</Count>
            <RetMax>3</RetMax>
            <RetStart>0</RetStart>
            <IdList>
                <Id>1001</Id>
                <Id>1002</Id>
                <Id>1003</Id>
            </IdList>
        </eSearchResult>"""
        mock_response = MagicMock()
        mock_response.content = xml_resp.encode("utf-8")
        mock_post.return_value = mock_response

        pmids, count = self.service._esearch_pmids_and_count("screen time", retmax=3, offset=0)
        self.assertEqual(count, 7746)
        self.assertEqual(pmids, ["1001", "1002", "1003"])

    @patch.object(PubMedService, "_retrieve_paper_details")
    @patch.object(PubMedService, "_esearch_pmids_and_count")
    def test_multipage_retrieval_beyond_previous_cap(self, mock_esearch, mock_details):
        """
        Verify that _fetch_papers paginates beyond 3,000 IDs up to the total count (e.g. 7,746).
        The previous code had fetch_limit=1000, max_attempts=3 (capped at 3,000).
        """
        total_count = 7746
        page1_ids = [str(i) for i in range(1, 5001)]       # 5,000 IDs
        page2_ids = [str(i) for i in range(5001, 7747)]    # 2,746 IDs

        def esearch_side_effect(query, retmax, offset):
            if offset == 0:
                return page1_ids, total_count
            elif offset == 5000:
                return page2_ids, total_count
            return [], total_count

        mock_esearch.side_effect = esearch_side_effect
        mock_details.side_effect = lambda pmids, cancel_event=None: [{"PMID": pid, "Title": f"Paper {pid}"} for pid in pmids]

        df = self.service._fetch_papers("screen time", max_results=10000)

        self.assertEqual(len(df), total_count)
        self.assertEqual(mock_esearch.call_count, 2)
        report = self.service.last_retrieval_report
        self.assertEqual(report["total_esearch_count"], 7746)
        self.assertEqual(report["pmids_retrieved"], 7746)
        self.assertEqual(report["records_fetched"], 7746)
        self.assertTrue(report["is_complete"])
        self.assertIsNone(report["warning"])

    @patch.object(PubMedService, "_retrieve_paper_details")
    @patch.object(PubMedService, "_esearch_pmids_and_count")
    def test_halting_at_requested_max_results(self, mock_esearch, mock_details):
        """When user requests max_results=500 and total_count=7,746, stop after 500 records."""
        total_count = 7746
        pmids_page = [str(i) for i in range(1, 501)]
        mock_esearch.return_value = (pmids_page, total_count)
        mock_details.side_effect = lambda pmids, cancel_event=None: [{"PMID": pid, "Title": f"Paper {pid}"} for pid in pmids]

        df = self.service._fetch_papers("screen time", max_results=500)

        self.assertEqual(len(df), 500)
        self.assertEqual(mock_esearch.call_count, 1)
        self.assertEqual(self.service.last_retrieval_report["pmids_retrieved"], 500)

    @patch.object(PubMedService, "_retrieve_paper_details")
    @patch.object(PubMedService, "_esearch_pmids_and_count")
    def test_halting_at_available_total_count(self, mock_esearch, mock_details):
        """When total_count=42 and user requests max_results=1000, retrieve all 42 without looping."""
        total_count = 42
        pmids = [str(i) for i in range(1, 43)]
        mock_esearch.return_value = (pmids, total_count)
        mock_details.side_effect = lambda p_list, cancel_event=None: [{"PMID": p, "Title": f"Paper {p}"} for p in p_list]

        df = self.service._fetch_papers("rare condition query", max_results=1000)

        self.assertEqual(len(df), 42)
        self.assertEqual(mock_esearch.call_count, 1)
        self.assertEqual(self.service.last_retrieval_report["total_esearch_count"], 42)
        self.assertEqual(self.service.last_retrieval_report["records_fetched"], 42)


class TestPubMedServiceEFetchReliability(unittest.TestCase):
    """Test retry with backoff, split-and-retry subdivision, and failure tracking."""

    def setUp(self):
        self.service = PubMedService(email="test@example.com", api_key="dummy_api_key")

    @patch("time.sleep", return_value=None)
    @patch.object(PubMedService, "_post_with_retry")
    def test_efetch_transient_failure_recovery(self, mock_post, mock_sleep):
        """Transient batch failure recovers on retry without losing records."""
        # First call fails, second call succeeds
        mock_success_resp = MagicMock()
        mock_success_resp.content = SAMPLE_PUBMED_ARTICLE_XML.encode("utf-8")

        mock_post.side_effect = [
            RuntimeError("Transient Connection Timeout"),
            mock_success_resp,
            MagicMock(json=lambda: {"result": {"uids": ["38000001"]}})  # summary call
        ]

        papers = self.service._fetch_batch_with_retry(["38000001"], max_batch_retries=3)

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["PMID"], "38000001")
        self.assertEqual(len(self.service._failed_pmids), 0)

    @patch("time.sleep", return_value=None)
    @patch.object(PubMedService, "_post_with_retry")
    def test_batch_subdivision_and_failure_reporting(self, mock_post, mock_sleep):
        """
        When a batch containing a problematic PMID fails all retries, subdivision
        isolates the failing PMID, rescues the valid PMIDs, and records the failure.
        """
        def post_side_effect(endpoint, data):
            ids = data.get("id", "").split(",")
            # If batch contains 9999, simulate persistent failure on efetch
            if endpoint == "efetch.fcgi":
                if "9999" in ids:
                    raise RuntimeError("NCBI EFetch 500 Internal Error for ID 9999")
                # Successful response for valid IDs
                xml_elements = []
                for pid in ids:
                    xml_elements.append(f"""<PubmedArticle>
                        <MedlineCitation><PMID>{pid}</PMID><Article><ArticleTitle>Title {pid}</ArticleTitle></Article></MedlineCitation>
                        <PubmedData><ArticleIdList><ArticleId IdType="pubmed">{pid}</ArticleId></ArticleIdList></PubmedData>
                    </PubmedArticle>""")
                content = f"<PubmedArticleSet>{''.join(xml_elements)}</PubmedArticleSet>"
                resp = MagicMock()
                resp.content = content.encode("utf-8")
                return resp
            elif endpoint == "esummary.fcgi":
                resp = MagicMock()
                resp.json.return_value = {"result": {"uids": ids}}
                return resp
            return MagicMock()

        mock_post.side_effect = post_side_effect

        batch_ids = ["101", "102", "9999", "104"]
        papers = self.service._fetch_batch_with_retry(batch_ids, max_batch_retries=2)

        # 3 valid papers rescued
        self.assertEqual(len(papers), 3)
        retrieved_pmids = [p["PMID"] for p in papers]
        self.assertIn("101", retrieved_pmids)
        self.assertIn("102", retrieved_pmids)
        self.assertIn("104", retrieved_pmids)
        self.assertNotIn("9999", retrieved_pmids)

        # 9999 logged as failed
        self.assertEqual(self.service._failed_pmids, ["9999"])
        self.assertEqual(self.service._failed_batches_count, 1)


class TestPubMedServiceXmlParsing(unittest.TestCase):
    """Test XML parsing of standard PubmedArticle, PubmedBookArticle, and mixed responses."""

    def setUp(self):
        self.service = PubMedService(email="test@example.com", api_key="dummy_api_key")

    def test_parse_pubmed_article(self):
        """Standard PubmedArticle XML parses into canonical dictionary."""
        papers = self.service._parse_pubmed_xml(SAMPLE_PUBMED_ARTICLE_XML.encode("utf-8"))
        self.assertEqual(len(papers), 1)
        p = papers[0]
        self.assertEqual(p["PMID"], "38000001")
        self.assertEqual(p["Title"], "Screen Time and Adolescent Mental Health")
        self.assertIn("association between screen time", p["Abstract"])
        self.assertEqual(p["DOI"], "10.2196/12345")
        self.assertEqual(p["PMCID"], "PMC1000001")
        self.assertEqual(p["Journal/Book"], "Journal of Medical Internet Research")
        self.assertEqual(p["Publication Year"], "2023")
        self.assertEqual(p["Authors"], ["Alice Smith", "Bob Johnson"])

    def test_parse_pubmed_book_article(self):
        """NCBI Bookshelf PubmedBookArticle XML parses into identical canonical schema."""
        papers = self.service._parse_pubmed_xml(SAMPLE_BOOK_ARTICLE_XML.encode("utf-8"))
        self.assertEqual(len(papers), 1)
        b = papers[0]
        self.assertEqual(b["PMID"], "38000002")
        self.assertEqual(b["Title"], "Chapter 1: Patterns of Screen Exposure in Early Childhood")
        self.assertIn("BACKGROUND: Digital screen exposure", b["Abstract"])
        self.assertEqual(b["DOI"], "10.1234/NBK54321.ch1")
        self.assertEqual(b["PMCID"], "PMC1000002")
        self.assertEqual(b["Journal/Book"], "Digital Media and Child Well-Being")
        self.assertEqual(b["Publication Year"], "2022")
        self.assertEqual(b["Authors"], ["David Williams"])
        self.assertIn("National Academies Press (US)", b["Citation"])
        self.assertIn("Digital Media and Child Well-Being", b["Citation"])

    def test_parse_mixed_articles(self):
        """Mixed XML payload with both PubmedArticle and PubmedBookArticle extracts all records."""
        papers = self.service._parse_pubmed_xml(SAMPLE_MIXED_ARTICLES_XML.encode("utf-8"))
        self.assertEqual(len(papers), 2)
        pmids = [p["PMID"] for p in papers]
        self.assertEqual(pmids, ["38000001", "38000002"])

        # Confirm identical key structure across both record types
        p_keys = set(papers[0].keys())
        b_keys = set(papers[1].keys())
        self.assertEqual(p_keys, b_keys)
        required_keys = {
            "Title", "Abstract", "Publication Year", "Source", "Journal/Book",
            "DOI", "Download_URL", "Keywords", "MeSH_Terms", "Authors",
            "Affiliations", "PMID", "Citation", "Create Date", "PMCID",
            "pmcid", "PDF_URL", "pdf_url", "Is_OA", "is_oa", "NIHMS ID",
            "First Author", "Reference"
        }
        self.assertTrue(required_keys.issubset(p_keys))


class TestPubMedServiceCandidatePreservationAndIsolation(unittest.IsolatedAsyncioTestCase):
    """Verify MedCPT reranking preserves candidate count and PubMed isolation."""

    def test_medcpt_candidate_preservation(self):
        """Re-ranking preserves total candidate count (head + unranked tail)."""
        reranker = MedCPTReRanker(max_candidates=10)
        # Mock models to avoid weight loading
        reranker._ensure_loaded = MagicMock(return_value=False)

        candidates = [{"PMID": str(i), "Title": f"Paper {i}", "Abstract": f"Abstract {i}"} for i in range(50)]
        ranked = reranker.rerank("screen time", candidates)
        self.assertEqual(len(ranked), 50)

    async def test_pubmed_search_isolation_does_not_call_openalex(self):
        """PubMed-only search mode does not invoke OpenAlex."""
        settings = Settings()
        search_service = SearchService(settings)

        with patch.object(search_service.unified_service.openalex_service, "search_works") as mock_oa:
            with patch.object(search_service, "_search_pubmed") as mock_pm:
                mock_pm.return_value = [{"PMID": "1001", "Title": "PubMed Paper"}]
                results = await search_service.search_papers(
                    query="screen time",
                    max_results=10,
                    search_source=SearchSource.PUBMED
                )
                self.assertEqual(len(results), 1)
                self.assertEqual(mock_pm.call_count, 1)
                mock_oa.assert_not_called()


class TestPubMedOptimizationAndReliability(unittest.TestCase):
    """Targeted tests for PMC enrichment, bounded retries, and MedCPT optimization."""

    def setUp(self):
        self.service = PubMedService(email="test@example.com", api_key="dummy_api_key")

    @patch("time.sleep", return_value=None)
    def test_pmc_enrichment_timeout_does_not_discard_records(self, mock_sleep):
        """PMC ID conversion timeout retains all records untouched and sets enrichment warning."""
        papers1 = [
            {"PMID": "1001", "Title": "Paper 1", "PMCID": ""},
            {"PMID": "1002", "Title": "Paper 2", "PMCID": ""},
        ]
        papers2 = [
            {"PMID": "1003", "Title": "Paper 3", "PMCID": ""},
            {"PMID": "1004", "Title": "Paper 4", "PMCID": ""},
        ]
        with patch.object(self.service.session, "get", side_effect=requests.exceptions.Timeout("Connection timed out")):
            self.service._enrich_pmc_ids(papers1)
            self.service._enrich_pmc_ids(papers2)  # second failing batch trips circuit breaker

        self.assertEqual(len(papers1), 2)
        self.assertEqual(papers1[0]["PMID"], "1001")
        self.assertEqual(papers1[1]["PMID"], "1002")
        self.assertTrue(self.service._pmc_circuit_broken)
        self.assertIsNotNone(self.service.last_enrichment_warning)
        self.assertIn("temporarily unavailable", self.service.last_enrichment_warning)

    @patch("time.sleep", return_value=None)
    def test_pmc_deduplication_prevents_unnecessary_reconversion(self, mock_sleep):
        """Previously queried PMIDs are tracked in _pmc_attempted_pmids and not requested again."""
        papers = [
            {"PMID": "2001", "Title": "Paper A", "PMCID": ""},
            {"PMID": "2002", "Title": "Paper B", "PMCID": ""},
        ]
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "records": [
                {"pmid": "2001", "pmcid": "PMC200100"},
                {"pmid": "2002", "pmcid": "PMC200200"},
            ]
        }
        with patch.object(self.service.session, "get", return_value=mock_resp) as mock_get:
            self.service._enrich_pmc_ids(papers)
            self.assertEqual(mock_get.call_count, 1)
            self.assertEqual(papers[0]["PMCID"], "PMC200100")

            # Calling again with the same papers must not call session.get
            self.service._enrich_pmc_ids(papers)
            self.assertEqual(mock_get.call_count, 1)

    @patch("time.sleep", return_value=None)
    @patch.object(PubMedService, "_post_with_retry")
    def test_retry_attempts_remain_within_configured_bounds(self, mock_post, mock_sleep):
        """A failing batch makes bounded requests without nested retry explosion."""
        mock_post.side_effect = RuntimeError("Persistent NCBI HTTP 500")

        # Failing batch of 2 PMIDs with max_depth=1
        self.service._fetch_batch_with_retry(["3001", "3002"], max_batch_retries=3, max_depth=1)

        # Depth 0 attempted max_batch_retries=3 times.
        # Depth 1 attempted 2 halves with max_batch_retries=1 each (2 calls).
        # Total calls = 3 + 2 = 5 calls (strictly <= 9 and nowhere near 567).
        self.assertLessEqual(mock_post.call_count, 9)
        self.assertEqual(mock_post.call_count, 5)

    @patch("time.sleep", return_value=None)
    @patch.object(PubMedService, "_post_with_retry")
    def test_recursive_subdivision_remains_bounded(self, mock_post, mock_sleep):
        """Subdivision depth is bounded by max_depth, preventing deep recursion."""
        mock_post.side_effect = RuntimeError("Persistent Network Error")

        # Batch of 8 PMIDs with max_depth=2
        pmids = [str(i) for i in range(4001, 4009)]
        self.service._fetch_batch_with_retry(pmids, max_batch_retries=2, max_depth=2)

        # Confirm all 8 failed PMIDs are recorded
        self.assertEqual(len(self.service._failed_pmids), 8)
        self.assertEqual(self.service._failed_pmids, pmids)
        self.assertGreater(self.service._failed_batches_count, 0)

    @patch("time.sleep", return_value=None)
    @patch.object(PubMedService, "_post_with_retry")
    @patch.object(PubMedService, "_esearch_pmids_and_count")
    def test_failed_pmids_reported_in_retrieval_report(self, mock_esearch, mock_post, mock_sleep):
        """Failed PMIDs are populated in the retrieval report and warning message."""
        mock_esearch.return_value = (["5001", "5002"], 2)
        mock_post.side_effect = RuntimeError("Simulated EFetch failure")

        df = self.service._fetch_papers("query", max_results=10)

        self.assertEqual(len(df), 0)
        report = self.service.last_retrieval_report
        self.assertFalse(report["is_complete"])
        self.assertEqual(report["failed_pmids"], ["5001", "5002"])
        self.assertIn("could not be retrieved", report["warning"])

    @patch.object(PubMedService, "_fetch_batch_with_retry")
    def test_successful_batches_not_fetched_again(self, mock_fetch_batch):
        """Successful batches are fetched exactly once in sequence."""
        mock_fetch_batch.side_effect = lambda pmids, cancel_event=None: [{"PMID": pid} for pid in pmids]

        pmids = [str(i) for i in range(100)]  # 100 PMIDs = exactly 2 batches of 50
        papers = self.service._retrieve_paper_details(pmids)

        self.assertEqual(len(papers), 100)
        self.assertEqual(mock_fetch_batch.call_count, 2)

    def test_medcpt_timing_and_candidate_count_preservation(self):
        """MedCPT reranker preserves candidate count and records load/inference duration."""
        reranker = MedCPTReRanker(max_candidates=5)

        # Mock query and article encoding
        import torch
        reranker._loaded = True
        reranker._torch = torch
        reranker.model_load_time_seconds = 0.42
        reranker._encode_query = MagicMock(return_value=torch.ones((1, 768)))
        reranker._encode_articles = MagicMock(return_value=torch.ones((5, 768)))

        candidates = [{"PMID": str(i), "Title": f"Title {i}", "Abstract": f"Abstract {i}"} for i in range(12)]
        results = reranker.rerank("query", candidates)

        self.assertEqual(len(results), 12)
        # Top 5 ranked with scores
        for r in results[:5]:
            self.assertIn("Relevance_Score", r)
            self.assertIn("Relevance_Rank", r)
        # Remaining 7 in tail preserved without error
        for r in results[5:]:
            self.assertNotIn("Relevance_Score", r)

        self.assertIsNotNone(reranker.last_inference_time_seconds)
        self.assertGreaterEqual(reranker.last_inference_time_seconds, 0)


if __name__ == "__main__":
    unittest.main()
