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
from backend.ocr.extract_boxes import extract_text_with_boxes
from backend.conversation.structure_visual import structure_visual_conversation



app = FastAPI(title="Chat Analysis AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Chat Analysis AI backend is running",
        "docs": "/docs"
    }



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

    # 2. Ingest raw text : # 3. Structure conversation
    if file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
       blocks, image_size = extract_text_with_boxes(file_path)
       conversation = structure_visual_conversation(blocks, image_size[0])
       speaker_detection = "visual"
    else:
       raw_text = ingest_file(file_path)
       conversation = structure_conversation(raw_text)
       speaker_detection = "text"
       
    conversation_length = len(conversation)


    # 4. Feature extraction
    participation = message_counts(conversation)
    linguistics = linguistic_features(conversation)

    a_count = participation.get("Person_A", {}).get("count", 0)
    b_count = participation.get("Person_B", {}).get("count", 0)

    if a_count == 0 or b_count == 0:
        signal_strength = 1
    else:
        ratio = min(a_count, b_count) / max(a_count, b_count)
        if ratio > 0.7:
              signal_strength = 3
        elif ratio > 0.4:
              signal_strength = 2
        else:
              signal_strength = 1




    # 5. Reasoning
    engagement = engagement_balance(participation)
    reciprocity = reciprocal_engagement(participation, linguistics)

    reasoning = {
        "engagement_balance": engagement,
        "reciprocal_engagement": reciprocity
    }

    # 6. Confidence
    confidence = confidence_score(
       conversation_length=conversation_length,
       signal_strength=signal_strength,
       speaker_detection=speaker_detection
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

