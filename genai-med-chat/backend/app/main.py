# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import chat, ingest, voice, ocr
from app.core.config import settings 

app = FastAPI(title="GenAI Medical Chat (local demo)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["ingest"])
app.include_router(voice.router, prefix="/api/v1", tags=["voice"])
app.include_router(ocr.router, prefix="/api/v1", tags=["ocr"])

@app.get("/")
def root():
    return {"service": "genai-med-chat", "mode": "local-demo"}
