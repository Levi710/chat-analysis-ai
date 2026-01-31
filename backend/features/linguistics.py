import re

def linguistic_features(conversation: list[dict]) -> dict:
    """
    Extracts simple linguistic features per speaker.
    """

    stats = {}

    for msg in conversation:
        speaker = msg["speaker"]
        text = msg["message"]

        if speaker not in stats:
            stats[speaker] = {
                "total_messages": 0,
                "total_length": 0,
                "question_count": 0,
                "emoji_count": 0
            }

        stats[speaker]["total_messages"] += 1
        stats[speaker]["total_length"] += len(text)
        stats[speaker]["question_count"] += text.count("?")
        stats[speaker]["emoji_count"] += len(re.findall(r"[^\w\s,\.]", text))

    # finalize averages
    for speaker, data in stats.items():
        data["avg_message_length"] = round(
            data["total_length"] / data["total_messages"], 2
        )

    return stats
