# backend/app/api/v1/ingest.py
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from typing import Optional

from app.services.ingest_service import IngestService

router = APIRouter()
ingest_service = IngestService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), user_id: int = Form(...), bg: BackgroundTasks = None):
    """
    Upload a document (pdf/txt/image). Ingest runs in background to OCR/chunk/embed/upsert.
    """
    if file.filename == "":
        raise HTTPException(status_code=400, detail="file required")

    # save file to disk
    saved_path = await ingest_service.save_upload(file, uploaded_by=user_id)

    # run ingestion in background (non-blocking)
    if bg:
        bg.add_task(ingest_service.ingest_file, saved_path, user_id)
        return {"status": "accepted", "filepath": saved_path}
    else:
        # synchronous fallback
        ingest_service.ingest_file(saved_path, user_id)
        return {"status": "ingested", "filepath": saved_path}
