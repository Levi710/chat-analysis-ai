import re

def normalize_text(raw_text: str) -> str:
    """
    Cleans OCR-extracted text while preserving meaning.
    """

    text = raw_text

    # remove excessive newlines
    text = re.sub(r"\n{2,}", "\n", text)

    # remove non-printable OCR artifacts
    text = re.sub(r"[¢©®™]", "", text)

    # normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()
