"""
Unit and integration tests for Research Rover PDF Download features.
Covers:
1. Verified open-access PDF downloads successfully.
2. PubMed paper with a PMC full-text PDF.
3. OpenAlex paper with an available open-access PDF.
4. Paper without available PDF displays a clear unavailable state.
5. Restricted paper paywall / 403 access control enforcement.
6. SSRF prevention, invalid URLs, and network error handling.
7. Unified Search PDF URL deduplication and merging.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.files import router, validate_safe_url, fetch_pdf_stream_safely
from app.services.unified_search_service import UnifiedSearchService
from app.core.config import Settings
from app.models.schemas import Paper


@pytest.fixture
def test_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# -----------------------------------------------------------------------------
# 1. SSRF & Security Validation Tests
# -----------------------------------------------------------------------------

def test_ssrf_rejects_private_ips(test_client):
    """Test that private and local IPs are rejected with HTTP 400."""
    private_urls = [
        "http://127.0.0.1:8000/secret.pdf",
        "http://localhost:8000/secret.pdf",
        "http://192.168.1.1/paper.pdf",
        "http://10.0.0.5/paper.pdf",
        "http://172.16.0.10/paper.pdf",
        "http://169.254.169.254/latest/meta-data/",
        "http://0.0.0.0/test.pdf",
    ]
    for url in private_urls:
        res = test_client.get(f"/download-pdf?url={url}")
        assert res.status_code == 400
        assert "forbidden" in res.json()["detail"].lower()


def test_ssrf_rejects_invalid_schemes(test_client):
    """Test that non-http/https schemes are rejected."""
    bad_schemes = [
        "file:///etc/passwd",
        "ftp://example.com/paper.pdf",
        "data:text/plain;base64,SGVsbG8=",
        "javascript:alert(1)",
    ]
    for url in bad_schemes:
        res = test_client.get(f"/download-pdf?url={url}")
        assert res.status_code == 400
        assert "scheme" in res.json()["detail"].lower() or "protocol" in res.json()["detail"].lower()


def test_ssrf_prevents_redirect_to_private_ip(test_client):
    """Test that a redirect pointing to a private IP is intercepted and blocked."""
    with patch("requests.Session.get") as mock_get:
        # First hop is public, but redirects to 127.0.0.1
        mock_resp = MagicMock()
        mock_resp.status_code = 302
        mock_resp.headers = {"Location": "http://127.0.0.1/internal-secret.pdf"}
        mock_get.return_value = mock_resp

        res = test_client.get("/download-pdf?url=https://example.com/redirect-me")
        assert res.status_code == 400
        assert "forbidden" in res.json()["detail"].lower()


# -----------------------------------------------------------------------------
# 2. Access Control / Paywall Enforcement Tests
# -----------------------------------------------------------------------------

def test_restricted_paper_enforces_access_control(test_client):
    """Test that a paywalled or restricted PDF (401/403) does not bypass access control."""
    with patch("requests.Session.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        mock_get.return_value = mock_resp

        res = test_client.get("/download-pdf?url=https://example.com/paywalled.pdf")
        assert res.status_code == 403
        assert "access restricted" in res.json()["detail"].lower() or "paywall" in res.json()["detail"].lower()


def test_remote_404_handled_gracefully(test_client):
    """Test that remote 404 is handled gracefully."""
    with patch("requests.Session.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_get.return_value = mock_resp

        res = test_client.get("/download-pdf?url=https://example.com/missing.pdf")
        assert res.status_code == 404
        assert "not found" in res.json()["detail"].lower()


def test_html_landing_page_rejected_as_non_pdf(test_client):
    """Test that HTML returned instead of PDF is detected and rejected with 422."""
    with patch("requests.Session.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "text/html; charset=utf-8"}
        mock_resp.iter_content.return_value = iter([b"<!DOCTYPE html><html><body>Login required</body></html>"])
        mock_get.return_value = mock_resp

        res = test_client.get("/download-pdf?url=https://example.com/abstract")
        assert res.status_code == 422
        assert "webpage" in res.json()["detail"].lower() or "direct pdf" in res.json()["detail"].lower()


# -----------------------------------------------------------------------------
# 3. Successful PDF Streaming & Header Tests
# -----------------------------------------------------------------------------

def test_successful_pdf_download_stream(test_client):
    """Test that a valid PDF streams correctly with content disposition and headers."""
    sample_pdf_bytes = b"%PDF-1.5 fake pdf content data chunk"
    with patch("requests.Session.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/pdf"}
        mock_resp.iter_content.return_value = iter([sample_pdf_bytes])
        mock_get.return_value = mock_resp

        res = test_client.get(
            "/download-pdf?url=https://example.com/valid.pdf"
            "&title=Machine Learning in Healthcare&doi=10.1000/182&pmid=12345"
        )
        assert res.status_code == 200
        assert res.headers["content-type"] == "application/pdf"
        assert 'attachment; filename="Machine_Learning_in_Healthcare.pdf"' in res.headers["content-disposition"]
        assert res.content == sample_pdf_bytes


# -----------------------------------------------------------------------------
# 4. PubMed PMC & OpenAlex Discovery Tests
# -----------------------------------------------------------------------------

def test_pubmed_pmc_pdf_url_discovery():
    """Test PubMedService properly identifies PMCID and constructs PMC PDF URL."""
    from app.services.pubmed_service import PubMedService
    service = PubMedService(email="test@example.com")
    
    # Mock papers list for _enrich_pmc_ids
    papers = [
        {"PMID": "34265844", "Title": "AlphaFold Paper"},
        {"PMID": "99999999", "Title": "No PMC Paper"}
    ]
    
    with patch("requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "records": [
                {"pmid": "34265844", "pmcid": "PMC8371605"}
            ]
        }
        mock_get.return_value = mock_resp
        
        service._enrich_pmc_ids(papers)
        
        assert papers[0].get("PMCID") == "PMC8371605"
        assert papers[0].get("PDF_URL") == "https://pmc.ncbi.nlm.nih.gov/articles/PMC8371605/pdf/"
        assert papers[0].get("Is_OA") is True
        assert papers[1].get("PMCID") is None
        assert papers[1].get("PDF_URL") is None


def test_openalex_pdf_url_discovery():
    """Test OpenAlexService prioritizes verified PDF URLs from best_oa_location."""
    from app.services.openalex_service import OpenAlexService
    settings = Settings(OPENALEX_API_KEY="test_key", EMAIL="test@example.com")
    service = OpenAlexService(settings=settings)

    raw_work = {
        "id": "https://openalex.org/W1234",
        "title": "Ethical AI",
        "best_oa_location": {
            "pdf_url": "https://arxiv.org/pdf/2009.10576",
            "landing_page_url": "http://arxiv.org/abs/2009.10576"
        },
        "open_access": {
            "is_oa": True,
            "oa_url": "http://arxiv.org/abs/2009.10576"
        },
        "ids": {}
    }

    parsed = service.parse_work_item(raw_work)
    assert parsed["PDF_URL"] == "https://arxiv.org/pdf/2009.10576"
    assert parsed["Is_OA"] is True
    assert parsed["Download_URL"] == "http://arxiv.org/abs/2009.10576"


def test_unified_search_merges_pdf_urls():
    """Test UnifiedSearchService merges PDF_URL from both sources."""
    settings = Settings(EMAIL="test@example.com")
    service = UnifiedSearchService(settings=settings)

    rec_pubmed = {
        "Title": "Cancer Research",
        "DOI": "10.1000/123",
        "Source": "PubMed",
        "PDF_URL": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12345/pdf/",
        "Is_OA": True
    }
    rec_openalex = {
        "Title": "Cancer Research",
        "DOI": "10.1000/123",
        "Source": "OpenAlex",
        "PDF_URL": "https://nature.com/articles/cancer.pdf",
        "Is_OA": True
    }

    merged = service.merge_paper_records(rec_pubmed, rec_openalex)
    assert merged["PDF_URL"] == "https://nature.com/articles/cancer.pdf"  # Direct .pdf preferred
    assert merged["Is_OA"] is True


def test_paper_model_pdf_unavailable_state():
    """Test Paper model correctly represents a paper without available PDF."""
    paper = Paper(
        source="pubmed",
        title="Restricted Paper Without OA",
        keywords=["cancer"],
        pdf_url=None,
        is_oa=False
    )
    assert paper.pdf_url is None
    assert paper.is_oa is False
