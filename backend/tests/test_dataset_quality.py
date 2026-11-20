"""
Comprehensive Unit Test Suite for Dataset Quality Assessment and Feature Readiness (Phase 2).
Tests cover:
1. Complete research-paper dataset (High quality, all features Ready)
2. Titles and abstracts with no affiliations (Country analysis Not Ready)
3. Affiliations with no keywords (Keyword & Co-occurrence Not Ready)
4. Titles only (Very low score, all advanced features Not Ready)
5. Missing abstracts (Semantic search and RAG Not Ready)
6. Duplicate paper records (Penalty applied, duplicate count verified)
7. Invalid publication years (Invalid value penalty, Trend analysis Not Ready)
8. Empty dataset (Score 0.0, Grade Critical, all features Not Ready)
9. Unmapped custom columns (Preserved, not penalized as errors)
10. Partial feature readiness (Coverage thresholds and warnings)
"""

import os
import sys
import unittest
import pandas as pd

# Add backend directory to sys.path so app modules import cleanly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.dataset_normalizer import DatasetNormalizer
from app.services.dataset_quality import (
    DatasetQualityAssessor,
    DatasetQualityReport,
    FeatureReadinessStatus,
    FeatureReadiness,
    FieldStatistics,
)


class TestDatasetQuality(unittest.TestCase):
    """Test suite for DatasetQualityAssessor."""

    def setUp(self):
        self.assessor = DatasetQualityAssessor()
        self.normalizer = DatasetNormalizer(fuzzy_threshold=0.85)

    # -----------------------------------------------------------------------
    # 1. Complete research-paper dataset
    # -----------------------------------------------------------------------
    def test_complete_research_paper_dataset(self):
        """Test assessment on a complete, high-quality research dataset."""
        data = {
            "Title": [
                "Deep Learning for Cancer Genomics",
                "Attention Is All You Need",
                "AlphaFold: High accuracy protein folding",
                "CRISPR-Cas9 Gene Editing Mechanisms",
                "Quantum Machine Learning in Healthcare",
            ],
            "Abstract": [
                "Deep neural networks have revolutionized cancer genomics through automated classification.",
                "The dominant sequence transduction models are based on neural networks and self-attention.",
                "Proteins are essential to life, and understanding their 3D structure is crucial.",
                "The CRISPR-associated Cas9 endonuclease enables RNA-guided precision genome engineering.",
                "We present a hybrid quantum-classical optimization algorithm for biomedical data.",
            ],
            "Authors": [
                "Smith, J.; Doe, A.",
                "Vaswani, A.; Shazeer, N.",
                "Jumper, J.; Evans, R.",
                "Doudna, J.; Charpentier, E.",
                "Preskill, J.; Lloyd, S.",
            ],
            "Affiliations": [
                "Harvard University, Cambridge, MA, USA",
                "Google Brain, Mountain View, CA, USA",
                "DeepMind, London, UK",
                "UC Berkeley, Berkeley, CA, USA",
                "Caltech, Pasadena, CA, USA",
            ],
            "Keywords": [
                "Deep Learning; Cancer; Genomics",
                "Transformer; Attention; Deep Learning",
                "AlphaFold; Protein Structure; Biology",
                "CRISPR; Cas9; Gene Editing",
                "Quantum; Healthcare; Machine Learning",
            ],
            "Publication Year": [2021, 2017, 2021, 2020, 2023],
            "DOI": [
                "10.1000/1",
                "10.1000/2",
                "10.1000/3",
                "10.1000/4",
                "10.1000/5",
            ],
            "Journal": ["Nature", "NeurIPS", "Nature", "Science", "Cell"],
            "Download_URL": [
                "https://example.com/1",
                "https://example.com/2",
                "https://example.com/3",
                "https://example.com/4",
                "https://example.com/5",
            ],
        }
        df = pd.DataFrame(data)
        report = self.assessor.assess_dataframe(df)

        self.assertEqual(report.total_records, 5)
        self.assertEqual(report.valid_records, 5)
        self.assertEqual(report.duplicate_records, 0)
        self.assertGreaterEqual(report.overall_quality_score, 90.0)
        self.assertEqual(report.quality_grade, "Excellent")

        # All 7 features should be READY
        for fid in [
            "keyword_analysis",
            "cooccurrence_analysis",
            "country_analysis",
            "author_analysis",
            "trend_analysis",
            "semantic_search",
            "ai_chat_rag",
        ]:
            self.assertEqual(
                report.feature_readiness[fid].status,
                FeatureReadinessStatus.READY,
                f"Feature {fid} should be READY",
            )

    # -----------------------------------------------------------------------
    # 2. Titles and abstracts with no affiliations
    # -----------------------------------------------------------------------
    def test_titles_and_abstracts_no_affiliations(self):
        """Test dataset with titles, abstracts, keywords, but zero affiliations."""
        data = {
            "Title": ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5"],
            "Abstract": [
                "Detailed abstract text explaining research methodology and findings 1.",
                "Detailed abstract text explaining research methodology and findings 2.",
                "Detailed abstract text explaining research methodology and findings 3.",
                "Detailed abstract text explaining research methodology and findings 4.",
                "Detailed abstract text explaining research methodology and findings 5.",
            ],
            "Keywords": [
                "AI; ML; NLP",
                "Robotics; Vision; AI",
                "Bioinformatics; Genomics",
                "Physics; Math; ML",
                "Chemistry; Molecules",
            ],
            "Publication Year": [2020, 2021, 2022, 2023, 2024],
        }
        df = pd.DataFrame(data)
        report = self.assessor.assess_dataframe(df)

        self.assertEqual(report.total_records, 5)
        # Country analysis must be NOT_READY
        self.assertEqual(
            report.feature_readiness["country_analysis"].status,
            FeatureReadinessStatus.NOT_READY,
        )
        # Semantic search and RAG should be READY
        self.assertEqual(
            report.feature_readiness["semantic_search"].status,
            FeatureReadinessStatus.READY,
        )
        self.assertEqual(
            report.feature_readiness["ai_chat_rag"].status,
            FeatureReadinessStatus.READY,
        )
        # Recommendation should mention affiliations
        self.assertTrue(any("Affiliation" in r for r in report.recommendations))

    # -----------------------------------------------------------------------
    # 3. Affiliations with no keywords
    # -----------------------------------------------------------------------
    def test_affiliations_no_keywords(self):
        """Test dataset with affiliations and abstracts, but zero keywords."""
        data = {
            "Title": ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5"],
            "Abstract": [
                "Abstract text covering clinical epidemiology and data analysis 1.",
                "Abstract text covering clinical epidemiology and data analysis 2.",
                "Abstract text covering clinical epidemiology and data analysis 3.",
                "Abstract text covering clinical epidemiology and data analysis 4.",
                "Abstract text covering clinical epidemiology and data analysis 5.",
            ],
            "Affiliations": [
                "Oxford University, Oxford, UK",
                "Stanford University, Stanford, CA, USA",
                "University of Tokyo, Tokyo, Japan",
                "Max Planck Institute, Berlin, Germany",
                "ETH Zurich, Zurich, Switzerland",
            ],
            "Publication Year": [2021, 2022, 2023, 2024, 2025],
        }
        df = pd.DataFrame(data)
        report = self.assessor.assess_dataframe(df)

        # Keyword features must be NOT_READY
        self.assertEqual(
            report.feature_readiness["keyword_analysis"].status,
            FeatureReadinessStatus.NOT_READY,
        )
        self.assertEqual(
            report.feature_readiness["cooccurrence_analysis"].status,
            FeatureReadinessStatus.NOT_READY,
        )
        # Country analysis should be READY
        self.assertEqual(
            report.feature_readiness["country_analysis"].status,
            FeatureReadinessStatus.READY,
        )
        # Recommendation should mention keywords
        self.assertTrue(any("Keyword" in r for r in report.recommendations))

    # -----------------------------------------------------------------------
    # 4. Titles only
    # -----------------------------------------------------------------------
    def test_titles_only(self):
        """Test minimal dataset with only paper titles."""
        data = {
            "Title": ["Paper Title A", "Paper Title B", "Paper Title C", "Paper Title D", "Paper Title E"],
        }
        df = pd.DataFrame(data)
        report = self.assessor.assess_dataframe(df)

        self.assertLessEqual(report.overall_quality_score, 30.0)
        self.assertIn(report.quality_grade, ("Poor", "Critical"))

        # Advanced features must be NOT_READY
        self.assertEqual(report.feature_readiness["keyword_analysis"].status, FeatureReadinessStatus.NOT_READY)
        self.assertEqual(report.feature_readiness["cooccurrence_analysis"].status, FeatureReadinessStatus.NOT_READY)
        self.assertEqual(report.feature_readiness["country_analysis"].status, FeatureReadinessStatus.NOT_READY)
        self.assertEqual(report.feature_readiness["trend_analysis"].status, FeatureReadinessStatus.NOT_READY)
        self.assertEqual(report.feature_readiness["semantic_search"].status, FeatureReadinessStatus.NOT_READY)
        self.assertEqual(report.feature_readiness["ai_chat_rag"].status, FeatureReadinessStatus.NOT_READY)

    # -----------------------------------------------------------------------
    # 5. Missing abstracts
    # -----------------------------------------------------------------------
    def test_missing_abstracts(self):
        """Test dataset with titles and keywords, but zero abstracts."""
        data = {
            "Title": ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5"],
            "Keywords": [
                "Machine Learning; AI",
                "Deep Learning; CNN",
                "Genomics; CRISPR",
                "Robotics; Control",
                "NLP; LLM",
            ],
            "Publication Year": [2021, 2022, 2023, 2024, 2025],
        }
        df = pd.DataFrame(data)
        report = self.assessor.assess_dataframe(df)

        # Semantic Search and RAG must be NOT_READY
        self.assertEqual(
            report.feature_readiness["semantic_search"].status,
            FeatureReadinessStatus.NOT_READY,
        )
        self.assertEqual(
            report.feature_readiness["ai_chat_rag"].status,
            FeatureReadinessStatus.NOT_READY,
        )
        # Keyword analysis should be READY
        self.assertEqual(
            report.feature_readiness["keyword_analysis"].status,
            FeatureReadinessStatus.READY,
        )
        # Recommendations should mention abstracts
        self.assertTrue(any("Abstract" in r for r in report.recommendations))

    # -----------------------------------------------------------------------
    # 6. Duplicate papers
    # -----------------------------------------------------------------------
    def test_duplicate_papers(self):
        """Test duplicate detection, penalty deduction, and recommendations."""
        data = {
            "Title": [
                "Paper Alpha",
                "Paper Alpha (Duplicate)",
                "Paper Beta",
                "Paper Beta (Duplicate)",
                "Paper Gamma",
            ],
            "DOI": [
                "10.1000/alpha",
                "10.1000/alpha",  # Duplicate of record 1
                "10.1000/beta",
                "10.1000/beta",   # Duplicate of record 3
                "10.1000/gamma",
            ],
            "Abstract": [
                "Abstract text for alpha.",
                "Abstract text for alpha duplicate.",
                "Abstract text for beta.",
                "Abstract text for beta duplicate.",
                "Abstract text for gamma.",
            ],
        }
        df = pd.DataFrame(data)
        report = self.assessor.assess_dataframe(df)

        self.assertEqual(report.total_records, 5)
        self.assertEqual(report.duplicate_records, 2)
        self.assertEqual(report.valid_records, 3)

        # Recommendation should mention duplicates
        self.assertTrue(any("duplicate" in r.lower() for r in report.recommendations))

    # -----------------------------------------------------------------------
    # 7. Invalid publication years
    # -----------------------------------------------------------------------
    def test_invalid_publication_years(self):
        """Test detection of invalid publication years and penalty deduction."""
        data = {
            "Title": ["Paper A", "Paper B", "Paper C", "Paper D", "Paper E"],
            "Abstract": [
                "Abstract for paper A.",
                "Abstract for paper B.",
                "Abstract for paper C.",
                "Abstract for paper D.",
                "Abstract for paper E.",
            ],
            "Year": ["invalid_year", "N/A", "9999", "-5", "not_a_number"],
        }
        df = pd.DataFrame(data)
        report = self.assessor.assess_dataframe(df)

        # Trend analysis must be NOT_READY
        self.assertEqual(
            report.feature_readiness["trend_analysis"].status,
            FeatureReadinessStatus.NOT_READY,
        )
        year_stat = report.field_statistics["publication_year"]
        self.assertEqual(year_stat.populated_records, 0)
        self.assertGreater(year_stat.invalid_records, 0)

        # Recommendation should warn about invalid years
        self.assertTrue(any("year" in r.lower() for r in report.recommendations))

    # -----------------------------------------------------------------------
    # 8. Empty dataset
    # -----------------------------------------------------------------------
    def test_empty_dataset(self):
        """Test assessment of a 0-row empty dataset."""
        df = pd.DataFrame()
        report = self.assessor.assess_dataframe(df)

        self.assertEqual(report.total_records, 0)
        self.assertEqual(report.overall_quality_score, 0.0)
        self.assertEqual(report.quality_grade, "Critical")

        # All features must be NOT_READY
        for fid in [
            "keyword_analysis",
            "cooccurrence_analysis",
            "country_analysis",
            "author_analysis",
            "trend_analysis",
            "semantic_search",
            "ai_chat_rag",
        ]:
            self.assertEqual(
                report.feature_readiness[fid].status,
                FeatureReadinessStatus.NOT_READY,
            )

    # -----------------------------------------------------------------------
    # 9. Unmapped custom columns
    # -----------------------------------------------------------------------
    def test_unmapped_columns(self):
        """Test that unmapped columns are tracked without unfair quality penalty."""
        data = {
            "Title": ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5"],
            "Abstract": [
                "Abstract covering scientific investigation and validation 1.",
                "Abstract covering scientific investigation and validation 2.",
                "Abstract covering scientific investigation and validation 3.",
                "Abstract covering scientific investigation and validation 4.",
                "Abstract covering scientific investigation and validation 5.",
            ],
            "Keywords": [
                "Deep Learning; NLP",
                "Computer Vision; AI",
                "Robotics; Control",
                "Data Science; ML",
                "Biomedical; Genetics",
            ],
            "Publication Year": [2021, 2022, 2023, 2024, 2025],
            "Lab_Bench_Number": ["B-101", "B-102", "B-103", "B-104", "B-105"],
            "Sample_Temperature_C": [37.0, 37.2, 36.8, 37.1, 37.0],
            "Internal_QC_Code": ["QC-PASS", "QC-PASS", "QC-PASS", "QC-PASS", "QC-PASS"],
        }
        df = pd.DataFrame(data)
        report = self.assessor.assess_dataframe(df)

        # Unmapped columns should be listed
        self.assertIn("Lab_Bench_Number", report.unmapped_columns)
        self.assertIn("Sample_Temperature_C", report.unmapped_columns)
        self.assertIn("Internal_QC_Code", report.unmapped_columns)
        self.assertEqual(len(report.unmapped_columns), 3)

        # Unmapped columns must NOT ruin the quality score (score should still be Good/Fair)
        self.assertGreaterEqual(report.overall_quality_score, 60.0)

    # -----------------------------------------------------------------------
    # 10. Partial feature readiness
    # -----------------------------------------------------------------------
    def test_partial_feature_readiness(self):
        """Test partial readiness with mixed coverage across features."""
        data = {
            "Title": [f"Paper {i}" for i in range(10)],
            # 3 papers have keywords (30% coverage)
            "Keywords": [
                "AI; ML",
                "Robotics",
                "Genomics",
                "",
                None,
                "",
                None,
                "",
                None,
                "",
            ],
            # 2 papers have affiliations (20% coverage)
            "Affiliations": [
                "Harvard University, Cambridge, MA, USA",
                "Oxford University, Oxford, UK",
                "",
                None,
                "",
                None,
                "",
                None,
                "",
                None,
            ],
            # 4 papers have abstracts (40% coverage)
            "Abstract": [
                "Abstract for paper 0 with adequate length.",
                "Abstract for paper 1 with adequate length.",
                "Abstract for paper 2 with adequate length.",
                "Abstract for paper 3 with adequate length.",
                "",
                None,
                "",
                None,
                "",
                None,
            ],
            # 1 single year
            "Publication Year": [2023] * 10,
        }
        df = pd.DataFrame(data)
        report = self.assessor.assess_dataframe(df)

        # Keyword analysis should be PARTIALLY_READY (30% coverage)
        self.assertEqual(
            report.feature_readiness["keyword_analysis"].status,
            FeatureReadinessStatus.PARTIALLY_READY,
        )
        # Co-occurrence should be NOT_READY (only 1 paper has 2+ keywords)
        self.assertEqual(
            report.feature_readiness["cooccurrence_analysis"].status,
            FeatureReadinessStatus.NOT_READY,
        )
        # Country analysis should be PARTIALLY_READY (20% coverage)
        self.assertEqual(
            report.feature_readiness["country_analysis"].status,
            FeatureReadinessStatus.PARTIALLY_READY,
        )
        # Semantic search should be PARTIALLY_READY (40% coverage)
        self.assertEqual(
            report.feature_readiness["semantic_search"].status,
            FeatureReadinessStatus.PARTIALLY_READY,
        )
        # Trend analysis should be PARTIALLY_READY (only 1 distinct year)
        self.assertEqual(
            report.feature_readiness["trend_analysis"].status,
            FeatureReadinessStatus.PARTIALLY_READY,
        )


if __name__ == "__main__":
    unittest.main()
