def build_analysis_prompt(
    question: str,
    participation: dict,
    linguistics: dict,
    reasoning: dict,
    confidence: dict
) -> str:
    """
    Builds a constrained prompt for LLM-based explanation.
    """

    return f"""
You are an analytical assistant.

You are given structured conversational metrics and rule-based conclusions.
You MUST NOT guess emotions, intentions, or internal states.
You MUST rely only on the provided data.

User Question:
{question}

Participation Metrics:
{participation}

Linguistic Metrics:
{linguistics}

Rule-Based Analysis:
{reasoning}

Confidence Assessment:
{confidence}

Instructions:
- Base your answer ONLY on the above data
- Cite specific evidence from metrics
- Explain reasoning step-by-step
- If evidence is weak, say so explicitly
- Do NOT claim feelings or intentions
- Keep tone neutral and professional

Respond in the following format:

Answer:
<short, cautious answer>

Evidence:
- <bullet point evidence>

Reasoning:
<concise explanation>

Confidence:
<label> (<numeric score>)

Disclaimer:
This analysis is based solely on observable chat behavior and does not infer internal feelings.
""".strip()
