"""
Unit tests for the Canonical Dataset Normalization Engine (Phase 1 Code Review).
Tests cover:
- PubMed, Scopus, Web of Science, OpenAlex, and custom schemas
- Exclusion of generic 'id' from keywords
- Conflicting scalar column mappings and non-destructive value preservation
- Fuzzy matching with ambiguity detection and confidence guardrails
- Distinction between unique record IDs and academic paper IDs
- Safe duplicate paper detection
- Rejection of invalid DOIs, URLs, and negative citations
- Conservative publication year parsing
- Non-destructive DataFrame normalization
- Safe Pydantic default factories
"""

import os
import sys
import unittest
import pandas as pd

# Add backend directory to sys.path so app modules import cleanly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.dataset_normalizer import (
    DatasetNormalizer,
    CanonicalPaperRecord,
    ColumnMapping,
    NormalizationReport,
    CANONICAL_FIELDS,
)


class TestDatasetNormalizer(unittest.TestCase):
    """Test suite for DatasetNormalizer following Phase 1 code review."""

    def setUp(self):
        self.normalizer = DatasetNormalizer(fuzzy_threshold=0.85)

    # -----------------------------------------------------------------------
    # 1. Standard PubMed-style CSV headers
    # -----------------------------------------------------------------------
    def test_pubmed_style_headers(self):
        """Test recognition and normalization of standard PubMed export headers."""
        data = {
            "Title": ["CRISPR Mechanisms in Gene Editing"],
            "Abstract": ["Comprehensive review of Cas9 endonuclease function."],
            "Authors": ["Doudna, Jennifer A.; Charpentier, Emmanuelle"],
            "Affiliations": ["UC Berkeley, CA, USA; Max Planck Institute, Berlin, Germany"],
            "Keywords": ["CRISPR; Cas9; Gene Editing"],
            "MeSH Terms": ["Endonucleases; RNA, Guide"],
            "Publication Year": ["2020"],
            "DOI": ["10.1126/science.1225829"],
            "PMID": ["22745249"],
            "Journal/Book": ["Science"],
            "Download_URL": ["https://science.org/doi/10.1126/science.1225829"],
            "Publication Date": ["2020-08-17"],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        self.assertEqual(rec.title, "CRISPR Mechanisms in Gene Editing")
        self.assertEqual(rec.abstract, "Comprehensive review of Cas9 endonuclease function.")
        self.assertIn("Doudna, Jennifer A.", rec.authors)
        self.assertIn("Charpentier, Emmanuelle", rec.authors)
        self.assertEqual(rec.publication_year, 2020)
        self.assertEqual(rec.doi, "10.1126/science.1225829")
        self.assertEqual(rec.pmid, "22745249")
        self.assertEqual(rec.journal, "Science")
        self.assertEqual(rec.download_url, "https://science.org/doi/10.1126/science.1225829")
        self.assertEqual(rec.publication_date, "2020-08-17")

        # Keywords and MeSH Terms both map to canonical 'keywords' and should be merged
        self.assertIn("CRISPR", rec.keywords)
        self.assertIn("Cas9", rec.keywords)
        self.assertIn("Endonucleases", rec.keywords)

        # Conflict on keywords should be reported
        self.assertTrue(any("keywords" in c for c in report.conflicts))

    # -----------------------------------------------------------------------
    # 2. Scopus-style headers
    # -----------------------------------------------------------------------
    def test_scopus_style_headers(self):
        """Test recognition and normalization of Scopus export headers."""
        data = {
            "Title": ["Deep Residual Learning for Image Recognition"],
            "Abstract": ["Deeper neural networks are more difficult to train."],
            "Authors": ["He, K.; Zhang, X.; Ren, S.; Sun, J."],
            "Affiliations": ["Microsoft Research, Beijing, China"],
            "Author Keywords": ["Deep learning; Residual networks"],
            "Index Keywords": ["Computer vision; Convolutional neural network"],
            "Year": ["2016"],
            "DOI": ["10.1109/CVPR.2016.90"],
            "Source title": ["Proceedings of the IEEE Computer Society Conference"],
            "Cited by": ["154230"],
            "Link": ["https://www.scopus.com/inward/record.uri?eid=2-s2.0-8499245"],
            "Document Type": ["Conference Paper"],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        self.assertEqual(rec.title, "Deep Residual Learning for Image Recognition")
        self.assertEqual(rec.publication_year, 2016)
        self.assertEqual(rec.citation_count, 154230)
        self.assertEqual(rec.journal, "Proceedings of the IEEE Computer Society Conference")
        self.assertEqual(rec.url, "https://www.scopus.com/inward/record.uri?eid=2-s2.0-8499245")
        self.assertEqual(rec.publication_type, "Conference Paper")
        # Keywords from both Author and Index keywords should be merged
        self.assertIn("Deep learning", rec.keywords)
        self.assertIn("Computer vision", rec.keywords)

    # -----------------------------------------------------------------------
    # 3. Web of Science-style headers
    # -----------------------------------------------------------------------
    def test_wos_style_headers(self):
        """Test recognition and normalization of Web of Science export headers."""
        data = {
            "Article Title": ["Attention Is All You Need"],
            "Abstract": ["The dominant sequence transduction models are based on neural networks."],
            "Authors": ["Vaswani, Ashish; Shazeer, Noam; Parmar, Niki"],
            "Addresses": ["Google Brain, Mountain View, CA 94043 USA"],
            "Author Keywords": ["Transformer; Attention Mechanism"],
            "Keywords Plus": ["Natural-Language Processing; Translation"],
            "Publication Year": ["2017"],
            "DOI": ["10.48550/arXiv.1706.03762"],
            "Source Title": ["Advances in Neural Information Processing Systems"],
            "Times Cited, WoS Core": ["84500"],
            "Doc Type": ["Article"],
            "UT (Unique WOS ID)": ["WOS:0004567890001"],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        self.assertEqual(rec.title, "Attention Is All You Need")
        self.assertIn("Google Brain, Mountain View, CA 94043 USA", rec.affiliations)
        self.assertEqual(rec.publication_year, 2017)
        self.assertEqual(rec.citation_count, 84500)
        self.assertEqual(rec.journal, "Advances in Neural Information Processing Systems")
        self.assertEqual(rec.publication_type, "Article")
        self.assertIn("Transformer", rec.keywords)
        self.assertIn("Natural-Language Processing", rec.keywords)
        self.assertEqual(rec.raw_data["UT (Unique WOS ID)"], "WOS:0004567890001")

    # -----------------------------------------------------------------------
    # 4. OpenAlex-style headers
    # -----------------------------------------------------------------------
    def test_openalex_style_headers(self):
        """Test recognition and normalization of OpenAlex tabular export headers."""
        data = {
            "display_name": ["AlphaFold: High accuracy protein structure prediction"],
            "abstract": ["Proteins are essential to life, and understanding their structure can facilitate a mechanistic understanding."],
            "author_names": ["Jumper, John; Evans, Richard; Pritzel, Alexander"],
            "concepts": ["Protein structure; AlphaFold; Computational biology"],
            "publication_year": ["2021"],
            "publication_date": ["2021-07-15"],
            "doi": ["https://doi.org/10.1038/s41586-021-03819-2"],
            "primary_location.source.display_name": ["Nature"],
            "cited_by_count": ["19800"],
            "openalex_id": ["https://openalex.org/W3178556885"],
            "is_oa": ["true"],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        self.assertEqual(rec.title, "AlphaFold: High accuracy protein structure prediction")
        self.assertEqual(rec.journal, "Nature")
        self.assertEqual(rec.publication_year, 2021)
        self.assertEqual(rec.publication_date, "2021-07-15")
        self.assertEqual(rec.doi, "10.1038/s41586-021-03819-2")
        self.assertEqual(rec.citation_count, 19800)
        self.assertEqual(rec.openalex_id, "https://openalex.org/W3178556885")
        self.assertTrue(rec.is_open_access)
        self.assertIn("Protein structure", rec.keywords)

    # -----------------------------------------------------------------------
    # 5. Custom headers (Paper_Name, Summary, Pub_Year, etc.)
    # -----------------------------------------------------------------------
    def test_custom_headers(self):
        """Test recognition of custom/informal headers."""
        data = {
            "Paper_Name": ["Advances in LLM Architectures"],
            "Summary": ["An empirical evaluation of mixture-of-experts."],
            "Pub_Year": ["2024"],
            "Citations": ["42"],
            "Paper_URL": ["https://example.com/papers/llm-moe.pdf"],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        self.assertEqual(rec.title, "Advances in LLM Architectures")
        self.assertEqual(rec.abstract, "An empirical evaluation of mixture-of-experts.")
        self.assertEqual(rec.publication_year, 2024)
        self.assertEqual(rec.citation_count, 42)
        self.assertEqual(rec.url, "https://example.com/papers/llm-moe.pdf")

    # -----------------------------------------------------------------------
    # 6. Headers with inconsistent capitalization and punctuation
    # -----------------------------------------------------------------------
    def test_inconsistent_capitalization_and_punctuation(self):
        """Test sanitization of messy headers with mixed case, dashes, underscores, and periods."""
        data = {
            "  tItLe  ": ["Messy Header Paper"],
            "AUTHOR-KEYWORDS (ALL)": ["AI; Neural Nets"],
            "YEAR / PUBLISHED...": ["2023"],
            "source - title": ["Journal of AI Research"],
            "doi:identifier": ["10.1000/182"],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        self.assertEqual(rec.title, "Messy Header Paper")
        self.assertIn("AI", rec.keywords)
        self.assertEqual(rec.publication_year, 2023)
        self.assertEqual(rec.journal, "Journal of AI Research")
        self.assertEqual(rec.doi, "10.1000/182")

    # -----------------------------------------------------------------------
    # 7. Missing optional columns
    # -----------------------------------------------------------------------
    def test_missing_optional_columns(self):
        """Test that missing optional fields do not raise errors and default gracefully."""
        data = {
            "Title": ["Minimal Dataset Paper"],
            "Abstract": ["Only title and abstract are provided."],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        self.assertEqual(rec.title, "Minimal Dataset Paper")
        self.assertEqual(rec.abstract, "Only title and abstract are provided.")
        self.assertEqual(rec.authors, [])
        self.assertEqual(rec.keywords, [])
        self.assertEqual(rec.affiliations, [])
        self.assertEqual(rec.countries, [])
        self.assertIsNone(rec.publication_year)
        self.assertIsNone(rec.doi)
        self.assertIsNone(rec.pmid)
        self.assertIsNone(rec.citation_count)
        self.assertIsNone(rec.is_open_access)
        self.assertEqual(rec.record_id, "record_1")
        self.assertEqual(rec.paper_id, "record_1")

    # -----------------------------------------------------------------------
    # 8. Duplicate or conflicting column mappings with scalar value preservation
    # -----------------------------------------------------------------------
    def test_duplicate_or_conflicting_column_mappings(self):
        """Test conflict detection, reporting, and non-destructive value preservation for scalar columns."""
        data = {
            "Title": ["Primary Title"],
            "Article Title": ["Alternative Title"],
            "Author Keywords": ["Deep Learning; Machine Learning"],
            "Index Keywords": ["Neural Networks; AI"],
            "DOI": ["10.1234/test-doi"],
            "Document DOI": ["10.1234/test-doi"],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        # Verify conflict is reported
        self.assertTrue(len(report.conflicts) >= 2)
        conflict_targets = [c.split(":")[0].strip() for c in report.conflicts]
        self.assertIn("title", conflict_targets)
        self.assertIn("keywords", conflict_targets)

        # List fields should be merged cleanly
        self.assertIn("Deep Learning", rec.keywords)
        self.assertIn("Neural Networks", rec.keywords)

        # Scalar fields: primary selected
        self.assertEqual(rec.title, "Primary Title")
        self.assertEqual(rec.doi, "10.1234/test-doi")

        # Scalar conflicting values MUST be preserved in conflicting_values
        self.assertIn("title", rec.conflicting_values)
        self.assertEqual(rec.conflicting_values["title"]["Title"], "Primary Title")
        self.assertEqual(rec.conflicting_values["title"]["Article Title"], "Alternative Title")

        # Original source columns MUST both be preserved in raw_data
        self.assertEqual(rec.raw_data["Title"], "Primary Title")
        self.assertEqual(rec.raw_data["Article Title"], "Alternative Title")
        self.assertEqual(rec.raw_data["Author Keywords"], "Deep Learning; Machine Learning")
        self.assertEqual(rec.raw_data["Index Keywords"], "Neural Networks; AI")

    # -----------------------------------------------------------------------
    # 9. Unknown columns preserved in raw_data
    # -----------------------------------------------------------------------
    def test_unknown_columns_preserved_in_raw_data(self):
        """Test that unrecognized or custom columns are preserved in raw_data and reported as unmapped."""
        data = {
            "Title": ["Custom Research Paper"],
            "Abstract": ["Some abstract text."],
            "Internal_Grant_Code": ["GRANT-2024-99"],
            "Lab_PI_Notes": ["High priority validation target"],
            "Temperature_Celsius": [37.5],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        self.assertEqual(report.unmapped_columns, 3)
        self.assertIn("Internal_Grant_Code", report.mappings)
        self.assertEqual(report.mappings["Internal_Grant_Code"].status, "unmapped")

        # Unmapped columns are fully preserved in raw_data
        self.assertEqual(rec.raw_data["Internal_Grant_Code"], "GRANT-2024-99")
        self.assertEqual(rec.raw_data["Lab_PI_Notes"], "High priority validation target")
        self.assertEqual(rec.raw_data["Temperature_Celsius"], 37.5)

    # -----------------------------------------------------------------------
    # 10. Empty values, invalid years, invalid DOIs, and negative citations
    # -----------------------------------------------------------------------
    def test_empty_values_and_invalid_publication_years(self):
        """Test robust handling of NaNs, missing strings, invalid DOIs, and negative citations."""
        data = {
            "Title": ["Paper A", None, "Paper C", "  "],
            "Abstract": [None, "Some abstract", "nan", "Real abstract"],
            "Year": ["invalid_year", "N/A", "9999", "2024-05-18"],
            "DOI": ["https://doi.org/10.1000/182", "doi: 10.1000/183", "invalid_doi_text", None],
            "Citation Count": ["15.0", "N/A", "-5", "100"],
            "Is_OA": ["true", "false", "unknown_val", None],
            "URL": ["https://example.com/paperA", "not a url", "ftp://example.org/doc", None],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 4)

        # Title fallback for None or whitespace
        self.assertEqual(records[0].title, "Paper A")
        self.assertEqual(records[1].title, "Unknown Title")
        self.assertEqual(records[2].title, "Paper C")
        self.assertEqual(records[3].title, "Unknown Title")

        # Abstract 'nan' string or None should become None
        self.assertIsNone(records[0].abstract)
        self.assertEqual(records[1].abstract, "Some abstract")
        self.assertIsNone(records[2].abstract)
        self.assertEqual(records[3].abstract, "Real abstract")

        # Publication year parsing
        self.assertIsNone(records[0].publication_year)  # "invalid_year" -> None
        self.assertIsNone(records[1].publication_year)  # "N/A" -> None
        self.assertIsNone(records[2].publication_year)  # 9999 is out of range -> None
        self.assertEqual(records[3].publication_year, 2024)  # "2024-05-18" -> 2024

        # Cleaned DOI: invalid_doi_text MUST be rejected to None
        self.assertEqual(records[0].doi, "10.1000/182")
        self.assertEqual(records[1].doi, "10.1000/183")
        self.assertIsNone(records[2].doi)  # "invalid_doi_text" -> None (not invented!)
        self.assertIsNone(records[3].doi)

        # Citation count: negative citations MUST be rejected to None
        self.assertEqual(records[0].citation_count, 15)
        self.assertIsNone(records[1].citation_count)
        self.assertIsNone(records[2].citation_count)  # "-5" -> None (invalid)
        self.assertEqual(records[3].citation_count, 100)

        # Is Open Access
        self.assertTrue(records[0].is_open_access)
        self.assertFalse(records[1].is_open_access)
        self.assertIsNone(records[2].is_open_access)
        self.assertIsNone(records[3].is_open_access)

        # Cleaned URL: "not a url" MUST be rejected to None
        self.assertEqual(records[0].url, "https://example.com/paperA")
        self.assertIsNone(records[1].url)
        self.assertEqual(records[2].url, "ftp://example.org/doc")
        self.assertIsNone(records[3].url)

    # -----------------------------------------------------------------------
    # 11. Distinction between unique record IDs and duplicate research-paper identifiers
    # -----------------------------------------------------------------------
    def test_duplicate_paper_identifiers(self):
        """Test distinction between record_id and paper_id, and duplicate tracking."""
        data = {
            "Title": ["First Copy", "Second Copy", "Unique Paper C", "No ID Paper D"],
            "DOI": ["10.1000/dup1", "10.1000/dup1", "10.1000/uniqC", None],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 4)

        # Each record has a distinct record_id
        self.assertEqual(records[0].record_id, "record_1")
        self.assertEqual(records[1].record_id, "record_2")
        self.assertEqual(records[2].record_id, "record_3")
        self.assertEqual(records[3].record_id, "record_4")

        # Papers with same DOI share paper_id
        self.assertEqual(records[0].paper_id, "10.1000/dup1")
        self.assertEqual(records[1].paper_id, "10.1000/dup1")
        self.assertFalse(records[0].is_duplicate)
        self.assertIsNone(records[0].duplicate_of)

        # Second occurrence is marked duplicate of record_1
        self.assertTrue(records[1].is_duplicate)
        self.assertEqual(records[1].duplicate_of, "record_1")

        # Third paper is unique
        self.assertFalse(records[2].is_duplicate)
        self.assertEqual(records[2].paper_id, "10.1000/uniqc")

        # Fourth paper has no DOI; fallback to record_4 without inventing fake DOI
        self.assertIsNone(records[3].doi)
        self.assertEqual(records[3].paper_id, "record_4")
        self.assertFalse(records[3].is_duplicate)

        # Report tracks duplicate count
        self.assertEqual(report.duplicate_records, 1)

    # -----------------------------------------------------------------------
    # 12. Ensure original dataframe remains unchanged
    # -----------------------------------------------------------------------
    def test_original_dataframe_unchanged(self):
        """Verify that normalize_dataframe does not mutate the source DataFrame."""
        original_data = {
            "Article Title": ["Sample Title 1", "Sample Title 2"],
            "Pub Year": ["2023", "2024"],
            "Authors": ["Smith, J.", "Doe, J."],
            "Custom_Col": [100, 200],
        }
        df = pd.DataFrame(original_data)
        df_copy_before = df.copy(deep=True)

        records, report = self.normalizer.normalize_dataframe(df)

        # Assert structure, columns, and data are strictly identical
        self.assertTrue(df.equals(df_copy_before))
        self.assertEqual(list(df.columns), list(df_copy_before.columns))
        self.assertEqual(df.iloc[0]["Article Title"], "Sample Title 1")

    # -----------------------------------------------------------------------
    # 13. Fuzzy matching: high confidence vs uncertain
    # -----------------------------------------------------------------------
    def test_fuzzy_matching(self):
        """Test that high-confidence typos match, while ambiguous or short headers are guarded."""
        data = {
            "Articel Title": ["Typo in Article Title"],  # High confidence typo (ratio 0.96)
            "Abstrct": ["Typo in Abstract"],            # High confidence typo (ratio 0.93)
            "Authers": ["Typo in Authors"],             # High confidence typo (ratio 0.93)
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        # Verify high-confidence fuzzy matching caught them as matched
        self.assertEqual(rec.title, "Typo in Article Title")
        self.assertEqual(rec.abstract, "Typo in Abstract")
        self.assertIn("Typo in Authors", rec.authors)

        self.assertEqual(report.mappings["Articel Title"].matching_method, "fuzzy_match")
        self.assertEqual(report.mappings["Articel Title"].status, "matched")

    # -----------------------------------------------------------------------
    # 14. Manual Custom Mappings Override
    # -----------------------------------------------------------------------
    def test_custom_mappings_override(self):
        """Test that explicit custom_mappings take precedence over automatic matching."""
        data = {
            "MySpecialColumn": ["This is actually the abstract content."],
            "Title": ["A Standard Title"],
        }
        df = pd.DataFrame(data)
        custom_mappings = {"MySpecialColumn": "abstract"}

        records, report = self.normalizer.normalize_dataframe(df, custom_mappings=custom_mappings)

        self.assertEqual(len(records), 1)
        rec = records[0]

        self.assertEqual(rec.abstract, "This is actually the abstract content.")
        self.assertEqual(report.mappings["MySpecialColumn"].matching_method, "manual_override")
        self.assertEqual(report.mappings["MySpecialColumn"].confidence, 1.0)

    # -----------------------------------------------------------------------
    # 15. Country column must NOT map to Affiliations
    # -----------------------------------------------------------------------
    def test_country_not_mapped_to_affiliations(self):
        """Rule verification: 'Country' must map to 'countries', NEVER to 'affiliations'."""
        data = {
            "Title": ["Country Mapping Paper"],
            "Affiliations": ["Harvard University, Cambridge, MA, USA"],
            "Country": ["United States"],
        }
        df = pd.DataFrame(data)
        records, report = self.normalizer.normalize_dataframe(df)

        self.assertEqual(len(records), 1)
        rec = records[0]

        # Country should map to canonical 'countries', NOT 'affiliations'
        self.assertEqual(report.mappings["Country"].canonical_field, "countries")
        self.assertEqual(report.mappings["Affiliations"].canonical_field, "affiliations")

        self.assertEqual(rec.countries, ["United States"])
        self.assertEqual(rec.affiliations, ["Harvard University, Cambridge, MA, USA"])

    # -----------------------------------------------------------------------
    # 16. Generic 'ID' must NOT map to Keywords
    # -----------------------------------------------------------------------
    def test_generic_id_not_mapped_to_keywords(self):
        """Rule verification: Generic 'id' or 'ID' column must NEVER map to keywords."""
        columns = ["ID", "id", "Record_ID", "Keywords"]
        mappings = self.normalizer.identify_mappings(columns)

        # "ID" and "id" must NOT map to "keywords"
        self.assertNotEqual(mappings["ID"].canonical_field, "keywords")
        self.assertNotEqual(mappings["id"].canonical_field, "keywords")

        # "Keywords" maps to keywords
        self.assertEqual(mappings["Keywords"].canonical_field, "keywords")

    # -----------------------------------------------------------------------
    # 17. Guard against fuzzy matching on short headers
    # -----------------------------------------------------------------------
    def test_short_headers_not_fuzzy_matched(self):
        """Rule verification: Short headers (< 4 chars) like 'id', 'di', 'ti' must not trigger false fuzzy matches."""
        columns = ["id", "di", "ti", "yr"]
        mappings = self.normalizer.identify_mappings(columns)

        # "id" should not fuzzy match "doi" or "di"
        self.assertNotEqual(mappings["id"].matching_method, "fuzzy_match")
        self.assertEqual(mappings["id"].status, "unmapped")

    # -----------------------------------------------------------------------
    # 18. Safe default factories on Pydantic models
    # -----------------------------------------------------------------------
    def test_pydantic_default_factories(self):
        """Verify that CanonicalPaperRecord uses safe default factories (no mutable shared defaults)."""
        rec1 = CanonicalPaperRecord()
        rec2 = CanonicalPaperRecord()

        # Mutate lists on rec1
        rec1.authors.append("Test Author")
        rec1.keywords.append("Test Keyword")
        rec1.raw_data["key"] = "value"

        # Assert rec2 is completely unaffected
        self.assertEqual(rec2.authors, [])
        self.assertEqual(rec2.keywords, [])
        self.assertEqual(rec2.raw_data, {})


if __name__ == "__main__":
    unittest.main()
