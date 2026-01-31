def confidence_score(conversation_length: int, signal_strength: int) -> dict:
    """
    Produces a confidence label and numeric score.
    """

    base = min(conversation_length / 20, 1.0)
    score = round(base * (signal_strength / 3), 2)

    if score >= 0.7:
        label = "high"
    elif score >= 0.4:
        label = "medium"
    else:
        label = "low"

    return {
        "score": score,
        "label": label
    }
