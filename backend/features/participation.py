from collections import Counter

def message_counts(conversation: list[dict]) -> dict:
    """
    Counts messages sent by each speaker.
    """

    counts = Counter()

    for msg in conversation:
        counts[msg["speaker"]] += 1

    total = sum(counts.values())

    return {
        speaker: {
            "count": count,
            "percentage": round(count / total, 2) if total > 0 else 0
        }
        for speaker, count in counts.items()
    }
