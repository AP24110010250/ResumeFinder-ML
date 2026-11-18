# Unit tests for PyMuPDF parser and candidate manager

import os
import sys
import fitz

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.resume_parser import validate_pdf, extract_pdf_text
from backend.candidate_manager import get_resume_hash, detect_duplicates


def test_parser():
    # Test valid PDF creation and extraction
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), "John Doe\nSoftware Engineer\nSkills: Python, Docker, SQL")
    pdf_bytes = doc.write()
    doc.close()

    is_valid, msg = validate_pdf(pdf_bytes)
    assert is_valid is True

    text, extract_msg = extract_pdf_text(pdf_bytes)
    assert extract_msg == "Success"
    assert "John Doe" in text
    assert "Python" in text

    # Test empty bytes
    is_valid_empty, empty_msg = validate_pdf(b"")
    assert is_valid_empty is False

    # Test file hashing
    h1 = get_resume_hash(pdf_bytes)
    h2 = get_resume_hash(pdf_bytes)
    assert h1 == h2


if __name__ == "__main__":
    test_parser()
    print("Parser tests passed successfully!")

