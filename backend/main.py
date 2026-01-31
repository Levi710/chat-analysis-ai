from fastapi import FastAPI, UploadFile, File, Form
import shutil
import uuid
import os

from backend.ingestion.router import ingest_file
from backend.conversation.structure import structure_conversation
from backend.features.participation import message_counts
from backend.features.linguistics import linguistic_features
from backend.reasoning.rules import engagement_balance, reciprocal_engagement
from backend.reasoning.confidence import confidence_score
from backend.llm.prompt_builder import build_analysis_prompt
from backend.llm.client import call_llm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Chat Analysis AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/analyze")
async def analyze_chat(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    # 1. Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Ingest raw text
    raw_text = ingest_file(file_path)

    # 3. Structure conversation
    conversation = structure_conversation(raw_text)

    # 4. Feature extraction
    participation = message_counts(conversation)
    linguistics = linguistic_features(conversation)

    # 5. Reasoning
    engagement = engagement_balance(participation)
    reciprocity = reciprocal_engagement(participation, linguistics)

    reasoning = {
        "engagement_balance": engagement,
        "reciprocal_engagement": reciprocity
    }

    # 6. Confidence
    confidence = confidence_score(
        conversation_length=len(conversation),
        signal_strength=2  # conservative default
    )

    # 7. Build LLM prompt (not calling LLM yet)
    prompt = build_analysis_prompt(
        question=question,
        participation=participation,
        linguistics=linguistics,
        reasoning=reasoning,
        confidence=confidence
    )

    llm_output = call_llm(prompt)

    return {
    "question": question,
    "analysis": llm_output,
    "confidence": confidence,
    "disclaimer": "This analysis is based solely on observable chat behavior and does not infer internal feelings."
    }

