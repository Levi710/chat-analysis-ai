from .normalize import normalize_text
from .segment import segment_messages

def structure_conversation(raw_text: str) -> list[dict]:
    """
    Converts raw text into structured conversation objects.
    """

    clean_text = normalize_text(raw_text)
    messages = segment_messages(clean_text)

    structured = []

    speakers = ["Person_A", "Person_B"]

    for i, msg in enumerate(messages):
        structured.append({
            "speaker": speakers[i % 2],
            "message": msg,
            "timestamp": None
        })

    return structured
