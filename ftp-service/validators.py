import os
import logging
from dataclasses import dataclass
import pandas as pd

from config import EXPECTED_HEADERS


@dataclass
class FileValidationResult:
    is_valid: bool
    status_code: int
    message: str


class FileValidator:
    SUCCESS = 200
    INVALID_FORMAT = 400
    INVALID_HEADERS = 401
    UNEXPECTED_HEADERS = 401
    EMPTY_FILE = 402
    PROCESSING_ERROR = 500

    @classmethod
    def validate_csv(cls, file_path: str) -> FileValidationResult:
        """Validates CSV file format and content"""
        try:
            if os.path.getsize(file_path) == 0:
                return FileValidationResult(False, cls.EMPTY_FILE, "File is empty")

            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                return FileValidationResult(False, cls.INVALID_FORMAT, f"Invalid CSV format: {str(e)}")

            if len(df) == 0:
                return FileValidationResult(False, cls.EMPTY_FILE, "CSV file has no data rows")

            headers = list(df.columns)
            missing_headers = [h for h in EXPECTED_HEADERS if h not in headers]
            if missing_headers:
                return FileValidationResult(
                    False, 
                    cls.INVALID_HEADERS,
                    f"Missing required headers: {', '.join(missing_headers)}"
                )

            extra_headers = [h for h in headers if h not in EXPECTED_HEADERS]
            if extra_headers:
                return FileValidationResult(
                    False,
                    cls.UNEXPECTED_HEADERS,
                    f"CSV contains unexpected headers: {', '.join(extra_headers)}"
                )

            return FileValidationResult(True, cls.SUCCESS, "CSV file is valid")

        except Exception as e:
            logging.error(f"Validation error: {str(e)}")
            return FileValidationResult(False, cls.PROCESSING_ERROR, f"Error validating CSV: {str(e)}")
