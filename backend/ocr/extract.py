import pytesseract
from .preprocess import preprocess_image

def extract_text_from_image(image_path: str) -> str:
    processed = preprocess_image(image_path)

    text = pytesseract.image_to_string(
        processed,
        config="--psm 6"
    )

    return text.strip()
