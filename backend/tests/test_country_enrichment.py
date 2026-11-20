"""
Unit tests for PubMed affiliation extraction, country extraction edge cases,
and CSV affiliation enrichment service (Part 11).
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.country_extractor import (
    extract_countries_from_affiliations,
    extract_countries_from_text,
    get_country_iso3,
)
from app.services.pubmed_service import PubMedService
from app.services.pubmed_affiliation_enricher import PubMedAffiliationEnricher


class TestCountryExtractionEdgeCases(unittest.TestCase):
    """Test suite for country extraction logic across various geographic formats."""

    def test_country_names(self):
        self.assertEqual(extract_countries_from_text("University of Delhi, India"), ["India"])
        self.assertEqual(extract_countries_from_text("Harvard University, United States"), ["United States"])
        self.assertEqual(extract_countries_from_text("Oxford University, United Kingdom"), ["United Kingdom"])
        self.assertEqual(extract_countries_from_text("University of Tokyo, Japan"), ["Japan"])

    def test_iso3_country_codes(self):
        self.assertIn("United Kingdom", extract_countries_from_text("Nottingham NHS Trust, Nottingham, GBR."))
        self.assertIn("India", extract_countries_from_text("Gauhati Medical College, Guwahati, IND."))
        self.assertIn("United States", extract_countries_from_text("Stanford University, Stanford, USA."))
        self.assertIn("China", extract_countries_from_text("Tsinghua University, Beijing, CHN."))

    def test_us_state_abbreviations(self):
        self.assertIn("United States", extract_countries_from_text("Harvard Medical School, Boston, MA"))
        self.assertIn("United States", extract_countries_from_text("Stanford University, Stanford, CA"))
        self.assertIn("United States", extract_countries_from_text("Columbia University, New York, NY"))
        # Ensure arbitrary words containing state letters do not cause false positives
        self.assertNotIn("United States", extract_countries_from_text("Department of insulin and immunology"))

    def test_geographic_aliases(self):
        self.assertIn("United Kingdom", extract_countries_from_text("University of Cambridge, UK"))
        self.assertIn("United States", extract_countries_from_text("MIT, Cambridge, U.S.A."))
        self.assertIn("South Korea", extract_countries_from_text("Seoul National University, Republic of Korea"))
        self.assertIn("South Korea", extract_countries_from_text("Yonsei University, Korea, Republic of"))


class TestPubMedAffiliationParsing(unittest.TestCase):
    """Test suite for PubMed XML affiliation extraction logic."""

    def setUp(self):
        self.service = PubMedService(email="test@example.com")

    def test_single_and_multiple_affiliations(self):
        xml_content = b"""<PubmedArticleSet>
            <PubmedArticle>
                <MedlineCitation>
                    <PMID>12345</PMID>
                    <Article>
                        <ArticleTitle>Test Article</ArticleTitle>
                        <AuthorList>
                            <Author>
                                <LastName>Doe</LastName>
                                <ForeName>John</ForeName>
                                <AffiliationInfo>
                                    <Affiliation>Department of CS, Stanford University, CA, USA.</Affiliation>
                                </AffiliationInfo>
                                <AffiliationInfo>
                                    <Affiliation>Department of Medicine, Oxford, UK.</Affiliation>
                                </AffiliationInfo>
                            </Author>
                            <Author>
                                <LastName>Smith</LastName>
                                <ForeName>Jane</ForeName>
                                <AffiliationInfo>
                                    <Affiliation>Department of CS, Stanford University, CA, USA.</Affiliation>
                                </AffiliationInfo>
                            </Author>
                        </AuthorList>
                    </Article>
                </MedlineCitation>
            </PubmedArticle>
        </PubmedArticleSet>"""
        papers = self.service._parse_pubmed_xml(xml_content)
        self.assertEqual(len(papers), 1)
        affs = papers[0]["Affiliations"]
        # Deduplicated: expected length 2
        self.assertEqual(len(affs), 2)
        self.assertIn("Department of CS, Stanford University, CA, USA.", affs)
        self.assertIn("Department of Medicine, Oxford, UK.", affs)

    def test_missing_affiliation(self):
        xml_content = b"""<PubmedArticleSet>
            <PubmedArticle>
                <MedlineCitation>
                    <PMID>67890</PMID>
                    <Article>
                        <ArticleTitle>Article Without Affiliations</ArticleTitle>
                        <AuthorList>
                            <Author>
                                <LastName>NoAff</LastName>
                                <ForeName>Author</ForeName>
                            </Author>
                        </AuthorList>
                    </Article>
                </MedlineCitation>
            </PubmedArticle>
        </PubmedArticleSet>"""
        papers = self.service._parse_pubmed_xml(xml_content)
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["Affiliations"], [])


class TestPubMedAffiliationEnricher(unittest.TestCase):
    """Test suite for PubMedAffiliationEnricher service using mocked API responses."""

    def setUp(self):
        self.enricher = PubMedAffiliationEnricher(email="test@example.com")

    @patch.object(PubMedService, "_post_with_retry")
    def test_enrichment_flow_mocked(self, mock_post):
        mock_xml = b"""<PubmedArticleSet>
            <PubmedArticle>
                <MedlineCitation>
                    <PMID>11111</PMID>
                    <Article>
                        <ArticleTitle>Paper 1</ArticleTitle>
                        <AuthorList>
                            <Author>
                                <LastName>Author</LastName>
                                <AffiliationInfo>
                                    <Affiliation>Department of Oncology, Tokyo, Japan.</Affiliation>
                                </AffiliationInfo>
                            </Author>
                        </AuthorList>
                    </Article>
                </MedlineCitation>
            </PubmedArticle>
        </PubmedArticleSet>"""
        mock_response = MagicMock()
        mock_response.content = mock_xml
        mock_post.return_value = mock_response

        df = pd.DataFrame([
            {"PMID": "11111", "Title": "Paper 1", "Affiliations": ""},
            {"PMID": "22222", "Title": "Paper 2", "Affiliations": "Existing Affiliation, London, UK"},
        ])

        temp_csv = "temp_test_enrichment.csv"
        df.to_csv(temp_csv, index=False, encoding="utf-8-sig")

        try:
            summary = self.enricher.enrich_csv(temp_csv, force=False, batch_size=50)
            self.assertEqual(summary["total_papers"], 2)
            self.assertEqual(summary["already_valid_before"], 1)
            self.assertEqual(summary["requested_from_pubmed"], 1)

            enriched_df = pd.read_csv(temp_csv)
            self.assertIn("Japan", str(enriched_df.at[0, "Affiliations"]))
            self.assertIn("London", str(enriched_df.at[1, "Affiliations"]))
        finally:
            for path in (temp_csv, temp_csv + ".backup", temp_csv + ".tmp"):
                if os.path.exists(path):
                    os.remove(path)


if __name__ == "__main__":
    unittest.main()
