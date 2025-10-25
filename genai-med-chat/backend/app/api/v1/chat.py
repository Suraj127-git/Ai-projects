# backend/app/api/v1/chat.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from app.services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    user_id: int
    text: str
    modalities: Optional[Dict] = None  # e.g., {"audio": False}

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[list] = []

@router.post("/query", response_model=ChatResponse)
async def query(req: ChatRequest, bg: BackgroundTasks):
    """
    Endpoint: synchronous retrieval + generate path (quick demo).
    For heavy ops (fine-tune / ingest), we offload to background tasks.
    """
    if not req.text:
        raise HTTPException(status_code=400, detail="text required")

    # For demo, call the service which may use Qdrant + model adapter
    resp = await chat_service.handle_query(req.user_id, req.text, modalities=req.modalities or {})
    return resp
