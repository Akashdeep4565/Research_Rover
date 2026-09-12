"""
Centralized CSV loading utility for Research Rover.

Provides robust, encoding-aware CSV file loading across the backend.
Automatically detects character encodings (UTF-8, UTF-8 with BOM,
Windows-1252, Latin-1/ISO-8859-1, etc.), handles safe fallbacks without
silently corrupting research data, and integrates with both pandas DataFrames
and standard Python csv row dictionaries.
"""

import codecs
import csv
import logging
import os
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

import charset_normalizer
import pandas as pd

logger = logging.getLogger("research_rover")

# Canonical candidate encodings to try in order when fallback is needed
CANDIDATE_FALLBACK_ENCODINGS: Tuple[str, ...] = (
    "utf-8",
    "utf-8-sig",
    "cp1252",
    "iso-8859-1",
    "cp1250",
    "cp1251",
    "latin1",
)

# Standard sample size for charset-normalizer (256 KB)
DEFAULT_SAMPLE_SIZE = 262144


class CSVLoadError(Exception):
    """Exception raised when a CSV file cannot be loaded or decoded."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        encoding: Optional[str] = None,
        original_error: Optional[Exception] = None,
    ):
        super().__init__(message)
        self.file_path = file_path
        self.encoding = encoding
        self.original_error = original_error


def check_bom(raw_bytes: bytes) -> Optional[str]:
    """
    Check if raw bytes start with a known Byte Order Mark (BOM).
    """
    if raw_bytes.startswith(codecs.BOM_UTF8):
        return "utf-8-sig"
    if raw_bytes.startswith(codecs.BOM_UTF16_LE):
        return "utf-16-le"
    if raw_bytes.startswith(codecs.BOM_UTF16_BE):
        return "utf-16-be"
    if raw_bytes.startswith(codecs.BOM_UTF32_LE):
        return "utf-32-le"
    if raw_bytes.startswith(codecs.BOM_UTF32_BE):
        return "utf-32-be"
    return None


def can_decode_file(
    file_path: str,
    encoding: str,
    chunk_size: int = 1048576,
    errors: str = "strict",
) -> bool:
    """
    Stream through the entire file using the given encoding to verify
    whether all bytes can be decoded without UnicodeDecodeError.
    """
    try:
        with open(file_path, "r", encoding=encoding, errors=errors) as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
        return True
    except (UnicodeDecodeError, UnicodeError, LookupError):
        return False
    except Exception as e:
        logger.debug("Error streaming file %s with %s: %s", file_path, encoding, e)
        return False


def normalize_encoding_name(encoding: Optional[str]) -> str:
    """
    Normalize encoding name to a standard Python codec name.
    """
    if not encoding:
        return "utf-8"
    enc = encoding.strip().lower().replace("_", "-")
    if enc in ("ascii", "utf-8", "utf8"):
        return "utf-8"
    if enc in ("utf-8-sig", "utf8-sig"):
        return "utf-8-sig"
    if enc in ("windows-1252", "cp1252", "ms-ansi"):
        return "cp1252"
    if enc in ("iso-8859-1", "latin-1", "latin1", "iso8859-1"):
        # For Western European text, cp1252 is a superset of iso-8859-1 that also
        # handles Windows smart quotes, dashes, and the Euro symbol correctly.
        return "cp1252"
    if enc in ("windows-1250", "cp1250"):
        return "cp1250"
    if enc in ("windows-1251", "cp1251"):
        return "cp1251"
    return enc


def detect_csv_encoding(
    file_path: str,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> str:
    """
    Automatically detect the character encoding of a CSV file.

    Strategy:
    1. Check for explicit BOM markers (e.g. UTF-8-SIG, UTF-16).
    2. Check if the file is completely valid strict UTF-8.
    3. Use charset-normalizer on a sample to inspect character patterns.
    4. Verify the candidate encoding by testing full-file decode compatibility.
    5. Test fallback encodings (cp1252, iso-8859-1, etc.) if needed.
    6. Log the detected encoding cleanly.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    file_size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)

    # Empty file default
    if file_size == 0:
        logger.info("Detected CSV encoding: utf-8 (empty file) for %s", filename)
        return "utf-8"

    # 1. Check BOM on initial bytes
    with open(file_path, "rb") as f:
        bom_sample = f.read(min(4, file_size))
    bom_enc = check_bom(bom_sample)
    if bom_enc:
        logger.info("Detected CSV encoding: %s (BOM header) for %s", bom_enc, filename)
        return bom_enc

    # 2. Check if the entire file is valid strict UTF-8
    if can_decode_file(file_path, "utf-8", errors="strict"):
        logger.info("Detected CSV encoding: utf-8 (valid UTF-8 stream) for %s", filename)
        return "utf-8"

    # 3. Read sample for inspection
    read_size = min(file_size, sample_size)
    with open(file_path, "rb") as f:
        sample_bytes = f.read(read_size)

    # Check for NUL bytes (UTF-16 without BOM)
    if b"\x00" in sample_bytes:
        for u16 in ("utf-16-le", "utf-16-be"):
            if can_decode_file(file_path, u16):
                logger.info("Detected CSV encoding: %s (NUL bytes detected) for %s", u16, filename)
                return u16

    # 4. Inspect with charset-normalizer
    detected_name = None
    coherence = 0.0
    try:
        detection = charset_normalizer.from_bytes(sample_bytes).best()
        if detection:
            detected_name = detection.encoding
            coherence = getattr(detection, "coherence", 0.0)
    except Exception as e:
        logger.warning("charset-normalizer failed on %s: %s", filename, e)
        detected_name = None

    normalized_detected = normalize_encoding_name(detected_name) if detected_name else None

    # If the file decodes cleanly under cp1252 (the standard for non-UTF8 Windows/Excel/PubMed CSVs):
    if can_decode_file(file_path, "cp1252"):
        # If charset-normalizer has high confidence in a specific non-Western encoding
        # (e.g. Cyrillic cp1251, Shift-JIS, etc.), honor that specific encoding:
        if (
            normalized_detected
            and normalized_detected not in ("cp1252", "utf-8", "big5", "mac-latin2", "cp1250")
            and coherence >= 0.2
        ):
            if can_decode_file(file_path, normalized_detected):
                logger.info(
                    "Detected CSV encoding: %s (high confidence %.2f) for %s",
                    normalized_detected,
                    coherence,
                    filename,
                )
                return normalized_detected

        logger.info("Detected CSV encoding: cp1252 (valid Windows-1252 stream) for %s", filename)
        return "cp1252"

    # If cp1252 failed (e.g. non-Latin bytes), verify detected candidate
    if normalized_detected and can_decode_file(file_path, normalized_detected):
        logger.info("Detected CSV encoding: %s for %s", normalized_detected, filename)
        return normalized_detected

    # 5. Try candidate fallbacks in prioritized order
    for candidate in CANDIDATE_FALLBACK_ENCODINGS:
        if candidate in ("utf-8", "cp1252"):
            continue
        if can_decode_file(file_path, candidate):
            logger.info(
                "Detected CSV encoding: %s (verified via fallback) for %s",
                candidate,
                filename,
            )
            return candidate

    # 6. Safe ultimate fallback (latin-1 can decode all 256 single-byte values)
    logger.warning(
        "No strict encoding could decode %s without error. Falling back to cp1252.",
        filename,
    )
    return "cp1252"


def read_csv_to_dataframe(
    csv_path: str,
    encoding: Optional[str] = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame using automatic encoding detection
    and multi-stage fallback error recovery.

    Preserves original characters (e.g. é, ó, ü, ñ, smart quotes) and handles
    CSV files from Excel, Scopus, PubMed, and Windows environments.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    filename = os.path.basename(csv_path)

    # If file is empty, return empty DataFrame or handle nrows=0 cleanly
    if os.path.getsize(csv_path) == 0:
        logger.info("CSV file is 0 bytes: %s, returning empty DataFrame", filename)
        return pd.DataFrame()

    # Determine primary encoding and candidates to try
    primary_encoding = encoding or detect_csv_encoding(csv_path)

    encodings_to_try: List[str] = [primary_encoding]
    for cand in CANDIDATE_FALLBACK_ENCODINGS:
        norm_cand = normalize_encoding_name(cand)
        if norm_cand not in encodings_to_try:
            encodings_to_try.append(norm_cand)

    last_error: Optional[Exception] = None

    # First pass: try strict decoding with candidate encodings
    for enc in encodings_to_try:
        try:
            call_kwargs = dict(kwargs)
            call_kwargs["encoding"] = enc
            df = pd.read_csv(csv_path, **call_kwargs)
            logger.debug("Successfully read CSV %s with encoding %s", filename, enc)
            return df
        except (UnicodeDecodeError, UnicodeError) as e:
            last_error = e
            logger.debug("Decoding with %s failed for %s: %s", enc, filename, e)
            continue
        except pd.errors.EmptyDataError:
            logger.warning("EmptyDataError reading CSV %s with %s", filename, enc)
            return pd.DataFrame()
        except Exception as e:
            # Re-raise non-encoding parser errors (unless caused by codec issues)
            last_error = e
            if "codec" in str(e).lower() or "decode" in str(e).lower():
                continue
            logger.error("Error reading CSV %s with %s: %s", filename, enc, e)
            raise CSVLoadError(
                f"Failed to parse CSV file '{filename}': {e}",
                file_path=csv_path,
                encoding=enc,
                original_error=e,
            ) from e

    # Last resort: only if all strict decodings failed
    logger.warning(
        "All strict encodings failed for %s. Attempting fallback with replacement characters.",
        filename,
    )
    for fallback_enc in ("cp1252", "utf-8"):
        try:
            call_kwargs = dict(kwargs)
            call_kwargs["encoding"] = fallback_enc
            call_kwargs["encoding_errors"] = "replace"
            df = pd.read_csv(csv_path, **call_kwargs)
            logger.warning(
                "Read %s using %s with encoding_errors='replace'", filename, fallback_enc
            )
            return df
        except Exception as e:
            last_error = e
            continue

    raise CSVLoadError(
        f"Unable to decode CSV file '{filename}'. The file may be corrupt or in an unsupported format.",
        file_path=csv_path,
        encoding=primary_encoding,
        original_error=last_error,
    ) from last_error


def read_csv_to_records(
    csv_path: str,
    encoding: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Read a CSV file into a list of row dictionaries (equivalent to csv.DictReader)
    using automatic encoding detection and fallback handling.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    filename = os.path.basename(csv_path)

    if os.path.getsize(csv_path) == 0:
        logger.info("CSV file is 0 bytes: %s, returning empty record list", filename)
        return []

    primary_encoding = encoding or detect_csv_encoding(csv_path)

    encodings_to_try: List[str] = [primary_encoding]
    for cand in CANDIDATE_FALLBACK_ENCODINGS:
        norm_cand = normalize_encoding_name(cand)
        if norm_cand not in encodings_to_try:
            encodings_to_try.append(norm_cand)

    last_error: Optional[Exception] = None

    for enc in encodings_to_try:
        try:
            with open(csv_path, "r", encoding=enc, newline="") as f:
                reader = csv.DictReader(f)
                records = list(reader)
                logger.debug("Successfully read %d records from %s with %s", len(records), filename, enc)
                return records
        except (UnicodeDecodeError, UnicodeError) as e:
            last_error = e
            logger.debug("DictReader decoding with %s failed for %s: %s", enc, filename, e)
            continue
        except Exception as e:
            last_error = e
            if "codec" in str(e).lower() or "decode" in str(e).lower():
                continue
            logger.error("Error reading CSV records from %s with %s: %s", filename, enc, e)
            raise CSVLoadError(
                f"Failed to parse CSV records from '{filename}': {e}",
                file_path=csv_path,
                encoding=enc,
                original_error=e,
            ) from e

    # Last resort fallback with replacement characters
    logger.warning(
        "All strict encodings failed for DictReader on %s. Attempting fallback with replacement characters.",
        filename,
    )
    for fallback_enc in ("cp1252", "utf-8"):
        try:
            with open(csv_path, "r", encoding=fallback_enc, errors="replace", newline="") as f:
                reader = csv.DictReader(f)
                records = list(reader)
                return records
        except Exception as e:
            last_error = e
            continue

    raise CSVLoadError(
        f"Unable to decode CSV file '{filename}' into records.",
        file_path=csv_path,
        encoding=primary_encoding,
        original_error=last_error,
    ) from last_error


@contextmanager
def open_csv_text(
    csv_path: str,
    mode: str = "r",
    newline: str = "",
    encoding: Optional[str] = None,
    **kwargs: Any,
) -> Iterator[Any]:
    """
    Context manager that yields an opened text file using the detected encoding.
    Ensures safe reading with proper encoding detection and clean file closure.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    enc = encoding or detect_csv_encoding(csv_path)
    f = open(csv_path, mode=mode, encoding=enc, newline=newline, **kwargs)
    try:
        yield f
    finally:
        f.close()
