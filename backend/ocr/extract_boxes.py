import pytesseract
from pytesseract import Output
from PIL import Image

def extract_text_with_boxes(image_path):
    image = Image.open(image_path)

    data = pytesseract.image_to_data(image, output_type=Output.DICT)

    blocks = []
    for i, text in enumerate(data["text"]):
        if text.strip():
            blocks.append({
                "text": text.strip(),
                "x": data["left"][i],
                "y": data["top"][i],
                "w": data["width"][i],
                "h": data["height"][i]
            })

    return blocks, image.size
