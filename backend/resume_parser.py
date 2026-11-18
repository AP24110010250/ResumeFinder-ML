# PDF Resume text extraction using PyMuPDF (fitz)

import fitz  # PyMuPDF


def validate_pdf(file_bytes):
    # Check if the uploaded file contains valid PDF data
    if not file_bytes:
        return False, "File is empty."

    try:
        # Attempt to open document stream
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page_count = doc.page_count
        doc.close()

        if page_count == 0:
            return False, "PDF contains no pages."

        return True, "Valid PDF file."
    except Exception as e:
        return False, f"Corrupted or invalid PDF file: {str(e)}"


def extract_pdf_text(file_bytes):
    # Extract text from every page of a PDF document using PyMuPDF
    is_valid, message = validate_pdf(file_bytes)
    if not is_valid:
        return "", message

    extracted_pages = []

    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page_text = page.get_text("text")
            if page_text:
                extracted_pages.append(page_text)
        doc.close()

        full_text = "\n".join(extracted_pages).strip()

        # Check if PDF lacks selectable text (e.g. scanned image PDF)
        if not full_text:
            return "", "PDF has no selectable text. Please upload a digital PDF with selectable text."

        return full_text, "Success"

    except Exception as e:
        return "", f"Error reading PDF content: {str(e)}"


def extract_resume_text(uploaded_file):
    # Read bytes from Streamlit uploaded file and extract text
    if uploaded_file is None:
        return "", "No file provided."

    file_bytes = uploaded_file.getvalue()
    text, message = extract_pdf_text(file_bytes)
    return text, message

