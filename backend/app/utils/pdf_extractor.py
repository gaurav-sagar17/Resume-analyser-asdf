"""
Safe PDF extraction utility for the Resume Analyzer.
Extracts only from bytes and never relies on file paths.
"""

from typing import Optional
import logging
import io

import pdfplumber
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> Optional[str]:
    """
    Extract text from a PDF entirely in memory.
    No file paths. No filename checks.
    Fully safe against weird Windows paths like 'resume?\'.
    """

    # Try pdfplumber first
    try:
        text_content = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)

        if text_content:
            return "\n".join(text_content)
    except Exception as e:
        logger.warning(f"pdfplumber failed, trying PyPDF2. Reason: {e}")

    # Fallback: PyPDF2
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text_content = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text:
                text_content.append(page_text)

        if text_content:
            return "\n".join(text_content)

        # If no text found
        raise ValueError("No extractable text found in the PDF.")

    except Exception as e:
        logger.error(f"Both extractors failed: {e}")
        raise ValueError("Failed to extract text from PDF. It may be scanned or corrupted.")
