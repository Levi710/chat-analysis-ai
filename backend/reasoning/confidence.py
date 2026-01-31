def confidence_score(
    conversation_length: int,
    signal_strength: int,
    speaker_detection: str
) -> dict:
    """
    Produces a confidence label and numeric score.
    speaker_detection: 'text' | 'visual'
    """

    # Base confidence from data volume
    base = min(conversation_length / 20, 1.0)

    # Signal-based scaling
    score = base * (signal_strength / 3)

    # Penalize heuristic speaker detection (screenshots)
    if speaker_detection == "visual":
        score *= 0.8   # downgrade confidence slightly

    score = round(score, 2)

    if score >= 0.7:
        label = "high"
    elif score >= 0.4:
        label = "medium"
    else:
        label = "low"

    return {
        "score": score,
        "label": label,
        "speaker_detection": speaker_detection
    }
