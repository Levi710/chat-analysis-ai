def segment_messages(text: str) -> list[str]:
    """
    Splits normalized text into individual message strings.
    """

    lines = text.split("\n")

    messages = []
    buffer = []

    for line in lines:
        if line.strip() == "":
            if buffer:
                messages.append(" ".join(buffer).strip())
                buffer = []
        else:
            buffer.append(line.strip())

    if buffer:
        messages.append(" ".join(buffer).strip())

    return messages
