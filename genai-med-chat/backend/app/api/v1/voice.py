from fastapi import APIRouter, UploadFile
import tempfile
import torch
from transformers import pipeline

router = APIRouter()

asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")

@router.post("/voice")
async def transcribe_audio(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = asr(tmp_path)["text"]
    return {"text": text}
