def engagement_balance(participation_features: dict) -> dict:
    """
    Determines whether engagement is balanced or skewed.
    """

    speakers = list(participation_features.keys())
    if len(speakers) < 2:
        return {
            "label": "insufficient_data",
            "reason": "Only one speaker detected"
        }

    p1, p2 = speakers[0], speakers[1]
    diff = abs(
        participation_features[p1]["percentage"] -
        participation_features[p2]["percentage"]
    )

    if diff <= 0.15:
        label = "balanced"
    elif participation_features[p1]["percentage"] > participation_features[p2]["percentage"]:
        label = f"{p1}_dominant"
    else:
        label = f"{p2}_dominant"

    return {
        "label": label,
        "difference": round(diff, 2)
    }

def reciprocal_engagement(participation: dict, linguistics: dict) -> dict:
    """
    Assesses reciprocal engagement based on observable signals.
    """

    speakers = list(participation.keys())
    if len(speakers) < 2:
        return {"label": "insufficient_data"}

    s1, s2 = speakers[0], speakers[1]

    msg_ratio_diff = abs(
        participation[s1]["percentage"] -
        participation[s2]["percentage"]
    )

    length_diff = abs(
        linguistics[s1]["avg_message_length"] -
        linguistics[s2]["avg_message_length"]
    )

    question_both = (
        linguistics[s1]["question_count"] > 0 and
        linguistics[s2]["question_count"] > 0
    )

    score = 0
    if msg_ratio_diff <= 0.15:
        score += 1
    if length_diff <= 30:
        score += 1
    if question_both:
        score += 1

    if score >= 2:
        label = "moderate_reciprocity"
    elif score == 1:
        label = "weak_reciprocity"
    else:
        label = "no_clear_reciprocity"

    return {
        "label": label,
        "signals": {
            "message_balance": msg_ratio_diff,
            "length_difference": length_diff,
            "both_ask_questions": question_both
        }
    }

