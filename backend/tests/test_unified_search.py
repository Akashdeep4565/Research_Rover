"""
Unit tests for UnifiedSearchService
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from app.core.config import Settings
from app.models.schemas import SearchSource
from app.services.unified_search_service import UnifiedSearchService

@pytest.fixture
def mock_settings():
    return Settings(
        OPENALEX_API_KEY="test_openalex_key",
        PUBMED_API_KEY="test_pubmed_key",
        EMAIL="test@example.com"
    )

@pytest.fixture
def unified_service(mock_settings):
    return UnifiedSearchService(settings=mock_settings)

def test_deduplicate_and_merge_by_doi(unified_service):
    pubmed_records = [
        {
            "Title": "Machine Learning in Cancer Research",
            "DOI": "10.1000/cancer123",
            "PMID": "12345678",
            "Source": "PubMed",
            "Source_Providers": ["pubmed"],
            "Publication Year": 2023,
            "Authors": ["Alice Smith"],
            "Affiliations": ["Harvard University"],
            "Countries": ["United States"]
        }
    ]
    openalex_records = [
        {
            "Title": "Machine Learning in Cancer Research",
            "DOI": "10.1000/cancer123",
            "OpenAlex_ID": "W9999",
            "Source": "OpenAlex",
            "Source_Providers": ["openalex"],
            "Publication Year": 2023,
            "Authors": ["Alice Smith"],
            "Affiliations": ["Harvard Medical School"],
            "Countries": ["United States"],
            "Citation_Count": 15,
            "Is_OA": True
        }
    ]

    merged = unified_service.deduplicate_and_merge(pubmed_records, openalex_records)
    assert len(merged) == 1
    record = merged[0]
    assert record["DOI"] == "10.1000/cancer123"
    assert record["PMID"] == "12345678"
    assert record["OpenAlex_ID"] == "W9999"
    assert record["Citation_Count"] == 15
    assert record["Is_OA"] is True

def test_deduplicate_and_merge_different_papers(unified_service):
    pubmed_records = [
        {
            "Title": "PubMed Only Paper",
            "DOI": "10.1000/pm1",
            "PMID": "111",
            "Source": "PubMed",
            "Source_Providers": ["pubmed"]
        }
    ]
    openalex_records = [
        {
            "Title": "OpenAlex Only Paper",
            "DOI": "10.1000/oa1",
            "OpenAlex_ID": "W222",
            "Source": "OpenAlex",
            "Source_Providers": ["openalex"]
        }
    ]

    merged = unified_service.deduplicate_and_merge(pubmed_records, openalex_records)
    assert len(merged) == 2

def test_execute_search_unified_partial_failure(unified_service):
    async def run():
        async def mock_pubmed_fetch(*args, **kwargs):
            raise Exception("PubMed Timeout Error")

        with patch.object(unified_service.openalex_service, "search_works", new_callable=AsyncMock) as mock_oa:
            mock_oa.return_value = [
                {
                    "Title": "OpenAlex Surviving Paper",
                    "DOI": "10.1000/survive",
                    "Source": "OpenAlex",
                    "source": "OpenAlex",
                    "Source_Providers": ["openalex"]
                }
            ]

            results = await unified_service.execute_search(
                query="cancer research",
                max_results=10,
                search_source=SearchSource.UNIFIED,
                pubmed_fetch_fn=mock_pubmed_fetch
            )

            assert len(results) == 1
            assert results[0]["Title"] == "OpenAlex Surviving Paper"

    asyncio.run(run())

def test_execute_search_pubmed_only(unified_service):
    async def run():
        async def mock_pubmed_fetch(*args, **kwargs):
            return [
                {
                    "Title": "PubMed Paper",
                    "DOI": "10.1000/pm",
                    "Source": "PubMed",
                    "source": "PubMed",
                    "Source_Providers": ["pubmed"]
                }
            ]

        with patch.object(unified_service.openalex_service, "search_works", new_callable=AsyncMock) as mock_oa:
            results = await unified_service.execute_search(
                query="test",
                max_results=10,
                search_source=SearchSource.PUBMED,
                pubmed_fetch_fn=mock_pubmed_fetch
            )

            assert len(results) == 1
            assert results[0]["Title"] == "PubMed Paper"
            mock_oa.assert_not_called()

    asyncio.run(run())
