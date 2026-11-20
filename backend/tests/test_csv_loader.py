"""
Comprehensive test suite for the Research Rover CSV loading utility
and encoding-resilient workflows using standard unittest.
"""

import asyncio
import codecs
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.csv_loader import (
    CSVLoadError,
    check_bom,
    detect_csv_encoding,
    read_csv_to_dataframe,
    read_csv_to_records,
    open_csv_text,
)
from app.services.search_service import SearchService
from app.services.analysis_service import AnalysisService
from app.core.config import get_settings


class TestCSVLoader(unittest.TestCase):
    """Unit tests for csv_loader utility functions."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_utf8_plain(self):
        """Test reading a standard UTF-8 CSV without BOM."""
        csv_path = os.path.join(self.temp_dir, "utf8_sample.csv")
        content = (
            "Title,Abstract,Source,Publication Year\n"
            "Deep Learning in Cancer,Study of deep neural networks,Nature,2024\n"
            "Genomic Analysis,High throughput sequencing,Science,2023\n"
        )
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(content)

        encoding = detect_csv_encoding(csv_path)
        self.assertEqual(encoding, "utf-8")

        df = read_csv_to_dataframe(csv_path)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ["Title", "Abstract", "Source", "Publication Year"])
        self.assertEqual(df.iloc[0]["Title"], "Deep Learning in Cancer")

        records = read_csv_to_records(csv_path)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["Title"], "Deep Learning in Cancer")

    def test_utf8_with_bom(self):
        """Test reading a UTF-8 CSV with BOM (utf-8-sig) ensuring column headers are clean."""
        csv_path = os.path.join(self.temp_dir, "utf8_bom.csv")
        content = (
            "Title,Abstract,Source,Publication Year\n"
            "BOM Test Paper,Evaluating UTF-8 with BOM,Lancet,2025\n"
        )
        with open(csv_path, "wb") as f:
            f.write(codecs.BOM_UTF8 + content.encode("utf-8"))

        encoding = detect_csv_encoding(csv_path)
        self.assertEqual(encoding, "utf-8-sig")

        df = read_csv_to_dataframe(csv_path)
        self.assertEqual(len(df), 1)
        # Crucial check: BOM must not contaminate the first column name
        self.assertEqual(df.columns[0], "Title")
        self.assertFalse(df.columns[0].startswith("\ufeff"))
        self.assertEqual(df.iloc[0]["Title"], "BOM Test Paper")

        records = read_csv_to_records(csv_path)
        self.assertEqual(len(records), 1)
        self.assertIn("Title", records[0])
        self.assertEqual(records[0]["Title"], "BOM Test Paper")

    def test_cp1252_with_accents_and_smart_quotes(self):
        """Test reading a Windows-1252 CSV containing accents (é, ó, ñ, ü), smart quotes, and dashes."""
        csv_path = os.path.join(self.temp_dir, "cp1252_sample.csv")
        content = (
            "Title,Abstract,Source,Publication Year\n"
            "Étude des algorithmes,“Modèle prédictif à l’hôpital — analyse”,Revue Médicale,2022\n"
            "Cáncer y diagnóstico,Investigación en niños y niñas con leucemia,Salud Pública,2023\n"
            "Über die Entwicklung,Präzisionsmedizin für Patienten,Medizin,2021\n"
        )
        with open(csv_path, "wb") as f:
            f.write(content.encode("cp1252"))

        # Confirm standard open('r', encoding='utf-8') would fail
        with self.assertRaises(UnicodeDecodeError):
            with open(csv_path, "r", encoding="utf-8") as f:
                f.read()

        # Confirm our loader handles it seamlessly
        encoding = detect_csv_encoding(csv_path)
        self.assertIn(encoding, ("cp1252", "iso-8859-1"))

        df = read_csv_to_dataframe(csv_path)
        self.assertEqual(len(df), 3)
        # Accented characters preserved
        self.assertEqual(df.iloc[0]["Title"], "Étude des algorithmes")
        self.assertTrue("—" in df.iloc[0]["Abstract"] or "analyse" in df.iloc[0]["Abstract"])
        self.assertEqual(df.iloc[1]["Title"], "Cáncer y diagnóstico")
        self.assertEqual(df.iloc[2]["Title"], "Über die Entwicklung")

        records = read_csv_to_records(csv_path)
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["Title"], "Étude des algorithmes")
        self.assertEqual(records[1]["Title"], "Cáncer y diagnóstico")
        self.assertEqual(records[2]["Title"], "Über die Entwicklung")

    def test_latin1_iso_8859_1(self):
        """Test reading an ISO-8859-1 (Latin-1) CSV."""
        csv_path = os.path.join(self.temp_dir, "latin1_sample.csv")
        content = (
            "Title,Abstract,Publication Year\n"
            "Télécommunication et Santé,Système d'alerte précoce,2020\n"
            "Señales biomédicas,Procesamiento digital de señales,2019\n"
        )
        with open(csv_path, "wb") as f:
            f.write(content.encode("iso-8859-1"))

        df = read_csv_to_dataframe(csv_path)
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]["Title"], "Télécommunication et Santé")
        self.assertEqual(df.iloc[1]["Title"], "Señales biomédicas")

        records = read_csv_to_records(csv_path)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["Title"], "Télécommunication et Santé")
        self.assertEqual(records[1]["Title"], "Señales biomédicas")

    def test_empty_csv(self):
        """Test reading a 0-byte CSV file without error."""
        csv_path = os.path.join(self.temp_dir, "empty.csv")
        with open(csv_path, "wb") as f:
            pass

        encoding = detect_csv_encoding(csv_path)
        self.assertEqual(encoding, "utf-8")

        df = read_csv_to_dataframe(csv_path)
        self.assertEqual(len(df), 0)

        records = read_csv_to_records(csv_path)
        self.assertEqual(len(records), 0)

    def test_open_csv_text_context_manager(self):
        """Test open_csv_text context manager with detected encoding."""
        csv_path = os.path.join(self.temp_dir, "ctx_test.csv")
        content = "Title,Year\nÉpithélium,2025\n"
        with open(csv_path, "wb") as f:
            f.write(content.encode("cp1252"))

        with open_csv_text(csv_path) as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
            self.assertIn("Épithélium", lines[1])

    def test_kwargs_passthrough(self):
        """Test that kwargs such as nrows and usecols pass through correctly."""
        csv_path = os.path.join(self.temp_dir, "kwargs_test.csv")
        content = (
            "ColA,ColB,ColC\n"
            "1,2,3\n"
            "4,5,6\n"
            "7,8,9\n"
        )
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(content)

        header_df = read_csv_to_dataframe(csv_path, nrows=0)
        self.assertEqual(len(header_df), 0)
        self.assertEqual(list(header_df.columns), ["ColA", "ColB", "ColC"])

        first_col_df = read_csv_to_dataframe(csv_path, usecols=[0])
        self.assertEqual(len(first_col_df), 3)
        self.assertEqual(list(first_col_df.columns), ["ColA"])


class TestBackendIntegration(unittest.TestCase):
    """Integration tests on actual backend services and real datasets."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_screen_time_dataset(self):
        """Test that screen_time_2001-2026.csv (which triggered the original UnicodeDecodeError) loads correctly."""
        settings = get_settings()
        file_path = os.path.join(settings.DATA_FOLDER, "screen_time_2001-2026.csv")
        if not os.path.exists(file_path):
            self.skipTest("screen_time_2001-2026.csv not found in data folder")

        # 1. detect_csv_encoding should detect cp1250, cp1252, or compatible
        enc = detect_csv_encoding(file_path)
        self.assertIn(enc, ("cp1250", "cp1252", "iso-8859-1", "cp850", "utf-8-sig", "utf-8"))

        # 2. read_csv_to_dataframe should load all 6,945 rows
        df = read_csv_to_dataframe(file_path)
        self.assertEqual(len(df), 6945)
        self.assertIn("Title", df.columns)
        self.assertIn("Abstract", df.columns)

        # 3. read_csv_to_records should load all rows
        records = read_csv_to_records(file_path)
        self.assertEqual(len(records), 6945)

    def test_search_service_load_papers_from_csv(self):
        """Test SearchService.load_papers_from_csv with a CP1252 encoded file."""
        settings = get_settings()
        search_service = SearchService(settings)

        csv_path = os.path.join(self.temp_dir, "search_cp1252.csv")
        content = (
            "Title,Abstract,Source,Publication Year,DOI,Authors,Keywords,Download_URL\n"
            "Étude biomédicale,Recherche sur l’oncologie pédiatrique,Oncologie,2023,10.1234/test1,['Dr. Dupuis'],['cancer; pediatric'],http://example.com/1\n"
            "Diagnóstico temprano,Análisis de datos médicos en el Perú,Salud,2024,10.1234/test2,['Dr. Gómez'],['datos; salud'],http://example.com/2\n"
        )
        with open(csv_path, "wb") as f:
            f.write(content.encode("cp1252"))

        papers = asyncio.run(search_service.load_papers_from_csv(csv_path))
        self.assertEqual(len(papers), 2)
        self.assertEqual(papers[0].title, "Étude biomédicale")
        self.assertEqual(papers[1].title, "Diagnóstico temprano")

    def test_analysis_service_normalize_metadata_cp1252(self):
        """Test AnalysisService.normalize_metadata with CP1252 encoded file."""
        settings = get_settings()
        analysis_service = AnalysisService(settings)

        csv_path = os.path.join(self.temp_dir, "analysis_cp1252.csv")
        content = (
            "Title,Abstract,Source,Publication Year,DOI,Keywords\n"
            'Präzisionsonkologie,Molekulare Diagnostik für Krebspatienten,Krebsforschung,2024,10.5555/k1,"[\'Onkologie\', \'Genomik\']"\n'
            'Cardiologie numérique,Télé-surveillance des arythmies,Cardio,2023,10.5555/k2,"[\'Arythmie\', \'Télémédecine\']"\n'
        )
        with open(csv_path, "wb") as f:
            f.write(content.encode("cp1252"))

        records = analysis_service.normalize_metadata(csv_path)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["title"], "Präzisionsonkologie")
        self.assertEqual(records[1]["title"], "Cardiologie numérique")


if __name__ == "__main__":
    unittest.main()
