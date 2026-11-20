"""
Pipeline tests for Research Rover Country Analysis.
Proves:
1. PubMed XML affiliation extraction works.
2. Affiliations are preserved when saving search results to CSV.
3. CountryService extracts countries from the generated CSV.
4. Country analysis uses the selected filename.
5. No fallback/demo dataset is accessed when affiliation data is missing.
6. Two different search-generated CSVs produce independent country-analysis results.
"""

import os
import sys
import tempfile
import shutil
import unittest
from xml.etree import ElementTree as ET

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.pubmed_service import PubMedService
from app.services.search_service import SearchService
from app.services.country_service import CountryService
from app.services.analysis_service import AnalysisService
from app.core.config import Settings
from fastapi.testclient import TestClient
from main import app


class TestCountryAnalysisPipeline(unittest.TestCase):
    """Pipeline integration test suite for topic-search generated CSV country analysis."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.settings = Settings(DATA_FOLDER=self.temp_dir)
        self.search_service = SearchService(self.settings)
        self.country_service = CountryService()
        self.analysis_service = AnalysisService(self.settings)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_pubmed_affiliation_extraction(self):
        """1. Prove PubMed XML affiliation extraction extracts <AffiliationInfo><Affiliation>."""
        xml_content = (
            b'<PubmedArticleSet>'
            b'<PubmedArticle>'
            b'  <MedlineCitation>'
            b'    <PMID>10001</PMID>'
            b'    <Article>'
            b'      <ArticleTitle>AI in Cancer Diagnostics</ArticleTitle>'
            b'      <Abstract><AbstractText>Deep learning methods.</AbstractText></Abstract>'
            b'      <Journal><Title>Cancer Informatics</Title></Journal>'
            b'      <AuthorList>'
            b'        <Author>'
            b'          <LastName>Smith</LastName><ForeName>John</ForeName>'
            b'          <AffiliationInfo>'
            b'            <Affiliation>Department of Oncology, Harvard Medical School, Boston, MA, USA.</Affiliation>'
            b'          </AffiliationInfo>'
            b'        </Author>'
            b'        <Author>'
            b'          <LastName>Chen</LastName><ForeName>Wei</ForeName>'
            b'          <AffiliationInfo>'
            b'            <Affiliation>Department of Medicine, Tsinghua University, Beijing, China.</Affiliation>'
            b'          </AffiliationInfo>'
            b'        </Author>'
            b'      </AuthorList>'
            b'    </Article>'
            b'  </MedlineCitation>'
            b'</PubmedArticle>'
            b'</PubmedArticleSet>'
        )

        service = PubMedService(email="test@example.com", api_key="dummy")
        papers = service._parse_pubmed_xml(xml_content)

        self.assertEqual(len(papers), 1)
        paper = papers[0]
        self.assertIn("Affiliations", paper)
        self.assertEqual(len(paper["Affiliations"]), 2)
        self.assertIn("Harvard Medical School, Boston, MA, USA.", paper["Affiliations"][0])
        self.assertIn("Tsinghua University, Beijing, China.", paper["Affiliations"][1])

    def test_affiliations_preserved_when_saving_csv(self):
        """2. Prove affiliations are saved into the generated search CSV."""
        import asyncio

        results = [
            {
                "Title": "AI Cancer Screening",
                "Abstract": "Screening model",
                "Publication Year": "2026",
                "Source": "Radiology",
                "DOI": "10.1000/123",
                "Download_URL": "https://pubmed.ncbi.nlm.nih.gov/10001/",
                "Authors": ["John Smith", "Wei Chen"],
                "Affiliations": [
                    "Harvard Medical School, Boston, MA, USA",
                    "Tsinghua University, Beijing, China",
                ],
                "PMID": "10001",
            }
        ]

        csv_path = os.path.join(self.temp_dir, "AI__cANCER.csv")
        asyncio.run(self.search_service.save_results_to_csv(results, csv_path))

        self.assertTrue(os.path.exists(csv_path))

        # Inspect CSV content directly
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        header = lines[0].strip()
        self.assertIn("Affiliations", header)

        content = "".join(lines)
        self.assertIn("Harvard Medical School", content)
        self.assertIn("USA", content)

    def test_country_service_extracts_countries_from_generated_csv(self):
        """3. Prove CountryService extracts countries from the generated CSV file."""
        import asyncio

        results = [
            {
                "Title": "Paper 1",
                "Authors": ["Author A"],
                "Affiliations": ["Sheba Medical Center, Israel"],
            },
            {
                "Title": "Paper 2",
                "Authors": ["Author B", "Author C"],
                "Affiliations": [
                    "Stanford University, USA",
                    "University of Cambridge, UK",
                ],
            },
        ]

        csv_path = os.path.join(self.temp_dir, "AI__cANCER.csv")
        asyncio.run(self.search_service.save_results_to_csv(results, csv_path))

        analysis = self.country_service.analyze_csv(csv_path)

        self.assertEqual(analysis["total_papers"], 2)
        self.assertEqual(analysis["papers_with_country_data"], 2)
        self.assertEqual(analysis["unique_countries"], 3)

        detected = {c["country"] for c in analysis["country_frequency"]}
        self.assertEqual(detected, {"Israel", "United States", "United Kingdom"})

        # Check collaboration graph
        collab = self.country_service.get_collaboration_graph_from_csv(csv_path)
        self.assertEqual(len(collab["nodes"]), 3)
        self.assertEqual(len(collab["links"]), 1)
        self.assertEqual(
            sorted([collab["links"][0]["source"], collab["links"][0]["target"]]),
            ["United Kingdom", "United States"],
        )

    def test_country_analysis_uses_selected_filename(self):
        """4. Prove Country Analysis API endpoint returns data for the specified filename."""
        import asyncio

        results = [
            {
                "Title": "Assamese Speech Study",
                "Authors": ["B. Sarma"],
                "Affiliations": ["Gauhati University, Guwahati, Assam, India"],
            }
        ]

        csv_name = "Assamese___speaker__idemtification.csv"
        csv_path = os.path.join(self.temp_dir, csv_name)
        asyncio.run(self.search_service.save_results_to_csv(results, csv_path))

        # Override DATA_FOLDER in app dependency
        from app.core.config import get_settings
        app.dependency_overrides[get_settings] = lambda: self.settings

        try:
            client = TestClient(app)
            res_stats = client.get(f"/api/v1/analysis/{csv_name}/countries")
            self.assertEqual(res_stats.status_code, 200)
            data_stats = res_stats.json()
            self.assertEqual(data_stats["filename"], csv_name)
            self.assertEqual(data_stats["countries"][0]["country"], "India")

            res_collab = client.get(f"/api/v1/analysis/{csv_name}/country-collaboration")
            self.assertEqual(res_collab.status_code, 200)
            data_collab = res_collab.json()
            self.assertEqual(data_collab["filename"], csv_name)
        finally:
            app.dependency_overrides.clear()

    def test_no_fallback_demo_dataset_accessed(self):
        """5. Prove that missing affiliation data yields 0 detected countries and NO fallback data."""
        import asyncio

        results = [
            {
                "Title": "Paper Without Affiliations",
                "Authors": ["Unknown Author"],
                "Affiliations": [],
            }
        ]

        csv_name = "no_affiliations.csv"
        csv_path = os.path.join(self.temp_dir, csv_name)
        asyncio.run(self.search_service.save_results_to_csv(results, csv_path))

        analysis = self.country_service.analyze_csv(csv_path)

        self.assertEqual(analysis["total_papers"], 1)
        self.assertEqual(analysis["papers_with_country_data"], 0)
        self.assertEqual(analysis["unique_countries"], 0)
        self.assertEqual(analysis["country_frequency"], [])
        self.assertEqual(analysis["collaboration_edges"], [])

    def test_independent_country_analysis_for_different_csvs(self):
        """6. Prove two different topic CSVs produce completely independent country results."""
        import asyncio

        # Topic 1 CSV
        csv1 = os.path.join(self.temp_dir, "topic_1.csv")
        asyncio.run(
            self.search_service.save_results_to_csv(
                [{"Title": "T1", "Affiliations": ["French National Centre, France"]}], csv1
            )
        )

        # Topic 2 CSV
        csv2 = os.path.join(self.temp_dir, "topic_2.csv")
        asyncio.run(
            self.search_service.save_results_to_csv(
                [{"Title": "T2", "Affiliations": ["German Cancer Research Center, Germany"]}], csv2
            )
        )

        res1 = self.country_service.analyze_csv(csv1)
        res2 = self.country_service.analyze_csv(csv2)

        countries1 = [c["country"] for c in res1["country_frequency"]]
        countries2 = [c["country"] for c in res2["country_frequency"]]

        self.assertEqual(countries1, ["France"])
        self.assertEqual(countries2, ["Germany"])
        self.assertNotEqual(countries1, countries2)


if __name__ == "__main__":
    unittest.main()
