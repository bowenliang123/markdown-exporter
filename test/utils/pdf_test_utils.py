import fitz


def extract_pdf_text(pdf_path: str) -> str:
    """Extract visible text from the first page of a PDF."""
    document = fitz.open(pdf_path)
    try:
        return document[0].get_text()
    finally:
        document.close()
