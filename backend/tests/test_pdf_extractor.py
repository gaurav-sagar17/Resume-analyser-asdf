"""
Tests for PDF extractor utility.
"""
import pytest
from app.utils.pdf_extractor import extract_text_from_pdf_bytes
import io


def test_extract_text_from_pdf_bytes_invalid():
    """Test extraction with invalid PDF bytes."""
    invalid_bytes = b"This is not a PDF file"
    
    with pytest.raises(ValueError):
        extract_text_from_pdf_bytes(invalid_bytes)


def test_extract_text_from_pdf_bytes_empty():
    """Test extraction with empty bytes."""
    empty_bytes = b""
    
    with pytest.raises(ValueError):
        extract_text_from_pdf_bytes(empty_bytes)

