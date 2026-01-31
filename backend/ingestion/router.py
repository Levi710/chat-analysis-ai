import os
from backend.ocr.extract import extract_text_from_image
from backend.document_extractor.pdf_extractor import extract_text_from_pdf
from backend.document_extractor.docx_extractor import extract_text_from_docx


def ingest_file(file_path: str) -> str:
    """
    Routes an input file to the appropriate text extractor.

    Args:
        file_path (str): Path to the uploaded file

    Returns:
        str: Extracted raw text
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)

    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)

    elif ext == ".docx":
        return extract_text_from_docx(file_path)

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    else:
        raise ValueError(f"Unsupported file type: {ext}")
