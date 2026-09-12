"""
Re-export centralized CSV loading utility for app package.
"""

from utils.csv_loader import (
    CSVLoadError,
    detect_csv_encoding,
    read_csv_to_dataframe,
    read_csv_to_records,
    open_csv_text,
    can_decode_file,
    check_bom,
    normalize_encoding_name,
)

__all__ = [
    "CSVLoadError",
    "detect_csv_encoding",
    "read_csv_to_dataframe",
    "read_csv_to_records",
    "open_csv_text",
    "can_decode_file",
    "check_bom",
    "normalize_encoding_name",
]
