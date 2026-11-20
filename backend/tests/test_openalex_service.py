"""
Unit tests for OpenAlexService
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import date
from app.core.config import Settings
from app.services.openalex_service import OpenAlexService

@pytest.fixture
def mock_settings():
    return Settings(
        OPENALEX_API_KEY="test_openalex_key",
        EMAIL="test@example.com"
    )

@pytest.fixture
def openalex_service(mock_settings):
    return OpenAlexService(settings=mock_settings)

def test_reconstruct_abstract(openalex_service):
    inverted_index = {
        "Machine": [0],
        "learning": [1],
        "in": [2],
        "healthcare.": [3]
    }
    abstract = openalex_service.reconstruct_abstract(inverted_index)
    assert abstract == "Machine learning in healthcare."

def test_reconstruct_abstract_empty(openalex_service):
    assert openalex_service.reconstruct_abstract(None) == ""
    assert openalex_service.reconstruct_abstract({}) == ""

def test_parse_openalex_work(openalex_service):
    raw_work = {
        "id": "https://openalex.org/W123456789",
        "title": "Deep Learning in Medical Imaging",
        "doi": "https://doi.org/10.1000/182",
        "publication_year": 2023,
        "cited_by_count": 42,
        "abstract_inverted_index": {
            "Medical": [0],
            "imaging": [1],
            "advancements.": [2]
        },
        "authorships": [
            {
                "author": {"display_name": "Jane Doe"},
                "countries": ["US"],
                "institutions": [{"display_name": "Harvard University"}]
            }
        ],
        "open_access": {
            "is_oa": True,
            "oa_url": "https://example.com/pdf.pdf"
        },
        "ids": {
            "pmid": "https://pubmed.ncbi.nlm.nih.gov/98765432"
        },
        "primary_location": {
            "source": {"display_name": "Journal of AI in Medicine"}
        }
    }

    parsed = openalex_service._parse_work(raw_work)
    assert parsed["Title"] == "Deep Learning in Medical Imaging"
    assert parsed["DOI"] == "10.1000/182"
    assert parsed["PMID"] == "98765432"
    assert parsed["OpenAlex_ID"] == "W123456789"
    assert parsed["Publication Year"] == "2023"
    assert parsed["Citation_Count"] == 42
    assert parsed["Is_OA"] is True
    assert parsed["PDF_URL"] == "https://example.com/pdf.pdf"
    assert parsed["Authors"] == ["Jane Doe"]
    assert "United States" in parsed["Countries"]
    assert "Harvard University" in parsed["Affiliations"]

def test_search_openalex_success(openalex_service):
    async def run():
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "https://openalex.org/W1111",
                    "title": "Test Paper",
                    "doi": "https://doi.org/10.1000/test",
                    "publication_year": 2022,
                    "cited_by_count": 10,
                    "authorships": [],
                    "open_access": {"is_oa": False, "oa_url": None},
                    "ids": {}
                }
            ]
        }

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            results = await openalex_service.search_papers(
                query="test query",
                max_results=5,
                start_date=date(2020, 1, 1),
                end_date=date(2023, 12, 31)
            )

            assert len(results) == 1
            assert results[0]["Title"] == "Test Paper"
            assert results[0]["OpenAlex_ID"] == "W1111"

            # Verify query parameters
            mock_get.assert_called_once()
            call_kwargs = mock_get.call_args.kwargs
            params = call_kwargs.get("params", {})
            assert params.get("search") == "test query"
            assert "from_publication_date:2020-01-01" in params.get("filter", "")
            assert "to_publication_date:2023-12-31" in params.get("filter", "")

    asyncio.run(run())

def test_search_openalex_error_resilience(openalex_service):
    async def run():
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = Exception("API Timeout")

            results = await openalex_service.search_papers(query="test", max_results=5)
            # Non-blocking error handling returns empty list
            assert results == []

    asyncio.run(run())
