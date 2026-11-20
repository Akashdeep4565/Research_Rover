import asyncio
import json
import os
import sys
import pandas as pd
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath("."))

from app.core.config import get_settings
from app.models.schemas import SearchRequest, SearchSource
from app.services.search_service import SearchService
from app.services.country_service import CountryService
from main import app

async def main():
    settings = get_settings()
    search_service = SearchService(settings)
    country_service = CountryService()
    client = TestClient(app)

    print("=" * 80)
    print("STEP 1: Performing real search for 'AI cancer'...")
    req1 = SearchRequest(
        query="AI cancer",
        max_results=10,
        search_source=SearchSource.PUBMED,
        use_raw_query=False
    )
    
    # Run search logic
    results1 = await search_service.search_papers(
        query=req1.query,
        max_results=req1.max_results,
        search_source=req1.search_source,
        use_raw_query=req1.use_raw_query
    )
    
    csv_filename1 = "AI__cANCER.csv"
    csv_path1 = os.path.join(settings.DATA_FOLDER, csv_filename1)
    await search_service.save_results_to_csv(results1, csv_path1)
    
    print(f"--> Saved {len(results1)} results to {csv_filename1}")
    print(f"--> File exists on disk: {os.path.exists(csv_path1)}")

    print("\nSTEP 2 & 3 & 4: Inspecting generated CSV columns and sample Affiliations:")
    df1 = pd.read_csv(csv_path1)
    print("CSV Columns:", list(df1.columns))
    self_contained_fields = ['Title', 'Authors', 'Affiliations', 'DOI', 'PMID']
    for field in self_contained_fields:
        print(f"  Field '{field}' in CSV: {field in df1.columns}")
        
    print("\n--- SAMPLE REAL AFFILIATIONS FROM AI__cANCER.csv ---")
    aff_samples = df1['Affiliations'].dropna().tolist()
    for idx, aff in enumerate(aff_samples[:5], 1):
        print(f"  [{idx}] {aff}")

    print("\nSTEP 5 & 6: Testing GET /api/v1/analysis/AI__cANCER.csv/countries")
    res_countries1 = client.get(f"/api/v1/analysis/{csv_filename1}/countries")
    print(f"Status: {res_countries1.status_code}")
    data_countries1 = res_countries1.json()
    print("Country Statistics Output:")
    print(f"  Total papers: {data_countries1.get('total_papers')}")
    print(f"  Papers with country data: {data_countries1.get('papers_with_country_data')}")
    print(f"  Unique countries: {data_countries1.get('unique_countries')}")
    print("  Top Countries Detected:")
    for c in data_countries1.get('countries', [])[:5]:
        print(f"    - {c['country']}: {c['frequency']} papers ({c['percentage']}%) [ISO: {c['iso_a3']}]")

    print("\nSTEP 7 & 8: Testing GET /api/v1/analysis/AI__cANCER.csv/country-collaboration")
    res_collab1 = client.get(f"/api/v1/analysis/{csv_filename1}/country-collaboration")
    print(f"Status: {res_collab1.status_code}")
    data_collab1 = res_collab1.json()
    print("Country Collaboration Output:")
    print(f"  Nodes count: {len(data_collab1.get('nodes', []))}")
    print(f"  Links count: {len(data_collab1.get('links', []))}")
    print("  Sample Links:")
    for link in data_collab1.get('links', [])[:5]:
        print(f"    - {link['source']} <--> {link['target']} (weight: {link['weight']})")

    print("\n" + "=" * 80)
    print("STEP 11 & 12: Performing second topic search for 'machine learning cancer'...")
    req2 = SearchRequest(
        query="machine learning cancer",
        max_results=10,
        search_source=SearchSource.PUBMED,
        use_raw_query=False
    )
    results2 = await search_service.search_papers(
        query=req2.query,
        max_results=req2.max_results,
        search_source=req2.search_source,
        use_raw_query=req2.use_raw_query
    )
    csv_filename2 = "machine_learning_cancer.csv"
    csv_path2 = os.path.join(settings.DATA_FOLDER, csv_filename2)
    await search_service.save_results_to_csv(results2, csv_path2)

    print(f"--> Saved {len(results2)} results to {csv_filename2}")
    res_countries2 = client.get(f"/api/v1/analysis/{csv_filename2}/countries")
    data_countries2 = res_countries2.json()
    print("Topic 2 Country Statistics Output:")
    print(f"  Total papers: {data_countries2.get('total_papers')}")
    print(f"  Papers with country data: {data_countries2.get('papers_with_country_data')}")
    print(f"  Unique countries: {data_countries2.get('unique_countries')}")
    for c in data_countries2.get('countries', [])[:5]:
        print(f"    - {c['country']}: {c['frequency']} papers ({c['percentage']}%)")

    print("\nSTEP 13 & 14: Verifying independence and empty-state handling:")
    # Empty affiliation CSV check
    no_aff_csv = "empty_affiliations_test.csv"
    no_aff_path = os.path.join(settings.DATA_FOLDER, no_aff_csv)
    pd.DataFrame([{
        "Title": "Paper without affiliations",
        "Authors": "['Author Anonymous']",
        "Affiliations": "[]"
    }]).to_csv(no_aff_path, index=False, encoding="utf-8-sig")

    res_empty = client.get(f"/api/v1/analysis/{no_aff_csv}/countries")
    data_empty = res_empty.json()
    print("Empty Affiliation CSV Test:")
    print(f"  Papers with country data: {data_empty.get('papers_with_country_data')}")
    print(f"  Countries list: {data_empty.get('countries')}")

    print("\nSUCCESS: End-to-end backend verification complete!")

if __name__ == "__main__":
    asyncio.run(main())
