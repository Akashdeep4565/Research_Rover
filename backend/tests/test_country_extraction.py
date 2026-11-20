"""
Unit test suite for backend country extraction and analysis layer.
Tests cover:
1. One affiliation -> one country
2. Multiple affiliations -> multiple countries
3. Multiple authors
4. Country aliases (USA, US, UK, PR China, etc.)
5. Missing affiliation (None, empty, NaN, malformed)
6. Unknown country
7. Duplicate countries within one paper
"""

import os
import sys
import tempfile
import shutil
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.country_extractor import (
    normalize_country_name,
    extract_countries_from_text,
    extract_countries_from_affiliations,
)
from app.services.country_service import CountryService


class TestCountryExtraction(unittest.TestCase):
    """Unit tests for country extraction and normalization utilities."""

    def test_one_affiliation_one_country(self):
        """Test parsing a single affiliation string containing one country."""
        aff = "Department of Computer Science, Stanford University, Stanford, CA, USA"
        countries = extract_countries_from_affiliations(aff)
        self.assertEqual(countries, ["United States"])

        aff2 = "Institute of Biochemistry, University of Zurich, Zurich, Switzerland"
        countries2 = extract_countries_from_affiliations(aff2)
        self.assertEqual(countries2, ["Switzerland"])

    def test_multiple_affiliations_multiple_countries(self):
        """Test parsing multiple affiliation strings from different countries."""
        affs = [
            "Department of Oncology, Harvard Medical School, Boston, MA, USA",
            "Nuffield Department of Medicine, University of Oxford, Oxford, UK",
            "Department of Biology, University of Tokyo, Tokyo, Japan",
        ]
        countries = extract_countries_from_affiliations(affs)
        self.assertEqual(countries, ["United States", "United Kingdom", "Japan"])

        # Multiple affiliations in a single string separated by semicolon
        semi_aff = "Department of Pathology, Paris, France; Department of Genetics, Berlin, Germany"
        semi_countries = extract_countries_from_affiliations(semi_aff)
        self.assertEqual(semi_countries, ["France", "Germany"])

    def test_multiple_authors(self):
        """Test extracting countries from multiple authors with structural/dict affiliations."""
        authors_data = [
            {"name": "Alice Smith", "affiliation": "Tsinghua University, Beijing, China"},
            {"name": "Bob Jones", "affiliation": "INSERM, Paris, France"},
            {"name": "Charlie Brown", "affiliation": "University of Toronto, Toronto, Canada"},
        ]
        countries = extract_countries_from_affiliations(authors_data)
        self.assertEqual(countries, ["China", "France", "Canada"])

    def test_country_aliases(self):
        """Test normalizing various country aliases and acronyms."""
        # USA variations
        self.assertEqual(normalize_country_name("USA"), "United States")
        self.assertEqual(normalize_country_name("US"), "United States")
        self.assertEqual(normalize_country_name("U.S.A."), "United States")
        self.assertEqual(normalize_country_name("United States of America"), "United States")

        # UK variations
        self.assertEqual(normalize_country_name("UK"), "United Kingdom")
        self.assertEqual(normalize_country_name("United Kingdom"), "United Kingdom")
        self.assertEqual(normalize_country_name("England"), "United Kingdom")
        self.assertEqual(normalize_country_name("Scotland"), "United Kingdom")

        # China variations
        self.assertEqual(normalize_country_name("PR China"), "China")
        self.assertEqual(normalize_country_name("People's Republic of China"), "China")
        self.assertEqual(normalize_country_name("China"), "China")

        # Text extraction alias test
        text_usa = "Harvard University, Cambridge, MA, USA"
        self.assertEqual(extract_countries_from_text(text_usa), ["United States"])

        text_uk = "Imperial College London, London, UK"
        self.assertEqual(extract_countries_from_text(text_uk), ["United Kingdom"])

    def test_missing_affiliation(self):
        """Test handling of None, empty strings, NaN, empty lists, and malformed strings gracefully."""
        self.assertEqual(extract_countries_from_affiliations(None), [])
        self.assertEqual(extract_countries_from_affiliations(""), [])
        self.assertEqual(extract_countries_from_affiliations([]), [])
        self.assertEqual(extract_countries_from_affiliations(float("nan")), [])
        self.assertEqual(extract_countries_from_affiliations("nan"), [])
        self.assertEqual(extract_countries_from_affiliations("[]"), [])
        self.assertEqual(extract_countries_from_affiliations("{}"), [])

    def test_unknown_country(self):
        """Test that unknown/arbitrary words are not misclassified as countries."""
        unknown_text = "Department of Quantum Physics, Institute of Unknown Science, Atlantis City"
        countries = extract_countries_from_affiliations(unknown_text)
        self.assertEqual(countries, [])

        # Ensure common words containing 'us', 'in', 'be', 'it' are not misclassified
        generic_text = "Analysis of viral status and cellular sinus in continuous locus"
        self.assertEqual(extract_countries_from_text(generic_text), [])

    def test_duplicate_countries_within_one_paper(self):
        """Test that duplicate mentions of the same country within a paper are deduplicated."""
        affs = [
            "Department of Biology, Harvard University, Boston, MA, USA",
            "Department of Physics, MIT, Cambridge, MA, USA",
            "Department of Medicine, Stanford University, Stanford, CA, United States",
        ]
        countries = extract_countries_from_affiliations(affs)
        self.assertEqual(countries, ["United States"])


class TestCountryService(unittest.TestCase):
    """Integration tests for CountryService methods and CSV integration."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.service = CountryService()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_country_service_analyze_records(self):
        """Test analyzing a list of paper records with collaboration network edges."""
        records = [
            {
                "Title": "Paper 1",
                "Affiliations": ["Harvard Univ, USA", "Oxford Univ, UK"],
            },
            {
                "Title": "Paper 2",
                "Affiliations": ["Tsinghua Univ, China", "Harvard Univ, USA"],
            },
            {
                "Title": "Paper 3",
                "Affiliations": ["Univ of Tokyo, Japan"],
            },
            {
                "Title": "Paper 4",
                "Affiliations": None,
            },
        ]

        result = self.service.analyze_records(records)
        self.assertEqual(result["total_papers"], 4)
        self.assertEqual(result["papers_with_country_data"], 3)
        self.assertEqual(result["unique_countries"], 4)

        freq_dict = {item["country"]: item["frequency"] for item in result["country_frequency"]}
        self.assertEqual(freq_dict["United States"], 2)
        self.assertEqual(freq_dict["United Kingdom"], 1)
        self.assertEqual(freq_dict["China"], 1)
        self.assertEqual(freq_dict["Japan"], 1)

        # Verify collaboration edges
        edges = result["collaboration_edges"]
        self.assertTrue(any(e["source"] == "United Kingdom" and e["target"] == "United States" and e["weight"] == 1 for e in edges))
        self.assertTrue(any(e["source"] == "China" and e["target"] == "United States" and e["weight"] == 1 for e in edges))

    def test_country_service_analyze_csv(self):
        """Test CountryService.analyze_csv reusing the centralized CSV loader."""
        csv_path = os.path.join(self.temp_dir, "country_test.csv")
        content = (
            "Title,Abstract,Source,Publication Year,Affiliations\n"
            '"Gene Therapy","Abstract 1","Journal A",2024,"[\'Stanford Univ, USA\', \'Imperial College, UK\']"\n'
            '"Vaccine Study","Abstract 2","Journal B",2023,"[\'INSERM, France\']"\n'
        )
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(content)

        result = self.service.analyze_csv(csv_path)
        self.assertEqual(result["total_papers"], 2)
        self.assertEqual(result["papers_with_country_data"], 2)
        freq_dict = {item["country"]: item["frequency"] for item in result["country_frequency"]}
        self.assertEqual(freq_dict["United States"], 1)
        self.assertEqual(freq_dict["United Kingdom"], 1)
        self.assertEqual(freq_dict["France"], 1)


class TestCountryCollaborationGraph(unittest.TestCase):
    """Test suite for country-level research collaboration graph requirements."""

    def setUp(self):
        self.service = CountryService()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_one_country_no_links(self):
        """Test paper with authors from only one country yields no links."""
        records = [
            {"Title": "Paper 1", "Affiliations": "AI Research Lab, IIT Delhi, India"}
        ]
        graph = self.service.get_collaboration_graph_from_records(records)
        self.assertEqual(len(graph["nodes"]), 1)
        self.assertEqual(graph["nodes"][0]["id"], "India")
        self.assertEqual(graph["nodes"][0]["paper_count"], 1)
        self.assertEqual(len(graph["links"]), 0)

    def test_two_countries_one_link(self):
        """Test paper with two countries yields exactly one collaboration link."""
        records = [
            {"Title": "Paper 1", "Affiliations": ["IIT Delhi, India", "MIT, USA"]}
        ]
        graph = self.service.get_collaboration_graph_from_records(records)
        self.assertEqual(len(graph["nodes"]), 2)
        self.assertEqual(len(graph["links"]), 1)
        link = graph["links"][0]
        self.assertEqual(sorted([link["source"], link["target"]]), ["India", "United States"])
        self.assertEqual(link["weight"], 1)

    def test_three_countries_three_links(self):
        """Test paper with three countries yields three unique collaboration links."""
        records = [
            {"Title": "Paper 1", "Affiliations": ["IIT Delhi, India", "MIT, USA", "Oxford, UK"]}
        ]
        graph = self.service.get_collaboration_graph_from_records(records)
        self.assertEqual(len(graph["nodes"]), 3)
        self.assertEqual(len(graph["links"]), 3)
        
        pairs = [tuple(sorted([link["source"], link["target"]])) for link in graph["links"]]
        self.assertIn(("India", "United States"), pairs)
        self.assertIn(("India", "United Kingdom"), pairs)
        self.assertIn(("United Kingdom", "United States"), pairs)

    def test_duplicate_countries_same_paper(self):
        """Test that multiple authors/affiliations from the same country do not create self-links or duplicate node counts."""
        records = [
            {
                "Title": "Paper 1",
                "Affiliations": [
                    "Department of CS, IIT Delhi, India",
                    "Department of AI, IISc Bangalore, India",
                    "Department of EE, IIT Bombay, India",
                ],
            }
        ]
        graph = self.service.get_collaboration_graph_from_records(records)
        self.assertEqual(len(graph["nodes"]), 1)
        self.assertEqual(graph["nodes"][0]["id"], "India")
        self.assertEqual(graph["nodes"][0]["paper_count"], 1)
        # Ensure country is not paired with itself
        self.assertEqual(len(graph["links"]), 0)

    def test_multiple_papers_increasing_collaboration_weight(self):
        """
        Test collaboration weight accumulation across multiple papers.
        Example:
          Paper 1: India + USA
          Paper 2: India + USA + UK
        Expected:
          India ↔ USA = 2
          India ↔ UK = 1
          USA ↔ UK = 1
          Nodes: India (2), USA (2), UK (1)
        """
        records = [
            {"Title": "Paper 1", "Affiliations": ["IIT Delhi, India", "MIT, USA"]},
            {"Title": "Paper 2", "Affiliations": ["IIT Delhi, India", "MIT, USA", "Oxford, UK"]},
        ]
        graph = self.service.get_collaboration_graph_from_records(records)
        
        node_counts = {node["id"]: node["paper_count"] for node in graph["nodes"]}
        self.assertEqual(node_counts["India"], 2)
        self.assertEqual(node_counts["United States"], 2)
        self.assertEqual(node_counts["United Kingdom"], 1)

        link_weights = {
            tuple(sorted([link["source"], link["target"]])): link["weight"]
            for link in graph["links"]
        }
        self.assertEqual(link_weights[("India", "United States")], 2)
        self.assertEqual(link_weights[("India", "United Kingdom")], 1)
        self.assertEqual(link_weights[("United Kingdom", "United States")], 1)

    def test_country_collaboration_api_endpoint(self):
        """Test GET /api/v1/analysis/{filename}/country-collaboration API endpoint."""
        from fastapi.testclient import TestClient
        from main import app
        from app.core.config import get_settings

        settings = get_settings()
        os.makedirs(settings.DATA_FOLDER, exist_ok=True)
        test_filename = "test_collab_api.csv"
        csv_path = os.path.join(settings.DATA_FOLDER, test_filename)

        content = (
            "Title,Abstract,Source,Publication Year,Affiliations\n"
            '"Study 1","Abstract 1","Journal A",2024,"[\'IIT Delhi, India\', \'Stanford, USA\']"\n'
            '"Study 2","Abstract 2","Journal B",2024,"[\'IIT Delhi, India\', \'Stanford, USA\', \'Oxford, UK\']"\n'
        )
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(content)

        try:
            client = TestClient(app)
            response = client.get(f"/api/v1/analysis/{test_filename}/country-collaboration")
            self.assertEqual(response.status_code, 200)
            data = response.json()

            self.assertEqual(data["filename"], test_filename)
            self.assertEqual(data["total_papers"], 2)
            self.assertEqual(data["papers_with_country_data"], 2)
            self.assertEqual(len(data["nodes"]), 3)
            self.assertEqual(len(data["links"]), 3)

            india_node = next(n for n in data["nodes"] if n["id"] == "India")
            self.assertEqual(india_node["paper_count"], 2)

            us_india_link = next(
                l for l in data["links"]
                if sorted([l["source"], l["target"]]) == ["India", "United States"]
            )
            self.assertEqual(us_india_link["weight"], 2)
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)

    def test_country_statistics_api_endpoint(self):
        """Test GET /api/v1/analysis/{filename}/countries API endpoint."""
        from fastapi.testclient import TestClient
        from main import app
        from app.core.config import get_settings

        settings = get_settings()
        os.makedirs(settings.DATA_FOLDER, exist_ok=True)
        test_filename = "test_country_stats_api.csv"
        csv_path = os.path.join(settings.DATA_FOLDER, test_filename)

        content = (
            "Title,Abstract,Source,Publication Year,Affiliations\n"
            '"Study 1","Abstract 1","Journal A",2024,"[\'IIT Delhi, India\', \'Stanford, USA\']"\n'
            '"Study 2","Abstract 2","Journal B",2024,"[\'IIT Delhi, India\', \'Oxford, UK\']"\n'
        )
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(content)

        try:
            client = TestClient(app)
            response = client.get(f"/api/v1/analysis/{test_filename}/countries")
            self.assertEqual(response.status_code, 200)
            data = response.json()

            self.assertEqual(data["filename"], test_filename)
            self.assertEqual(data["total_papers"], 2)
            self.assertEqual(data["papers_with_country_data"], 2)
            self.assertEqual(data["unique_countries"], 3)

            c_map = {item["country"]: item for item in data["countries"]}
            self.assertIn("India", c_map)
            self.assertEqual(c_map["India"]["frequency"], 2)
            self.assertEqual(c_map["India"]["percentage"], 100.0)
            self.assertEqual(c_map["United States"]["frequency"], 1)
            self.assertEqual(c_map["United States"]["percentage"], 50.0)
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)


if __name__ == "__main__":
    unittest.main()


