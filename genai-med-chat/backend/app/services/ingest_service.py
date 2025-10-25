# backend/app/services/ingest_service.py
import os
from pathlib import Path
from typing import Optional
from uuid import uuid4
from app.core.config import settings

# optional OCR libraries will be used if installed
try:
    import pytesseract
    from PIL import Image
except Exception:
    pytesseract = None

# langchain utilities if available
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import Qdrant
except Exception:
    RecursiveCharacterTextSplitter = None
    HuggingFaceEmbeddings = None
    Qdrant = None

class IngestService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.qdrant = None
        if Qdrant and HuggingFaceEmbeddings:
            try:
                emb = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
                self.qdrant = Qdrant(url=settings.QDRANT_URL, prefer_grpc=False, collection_name=settings.QDRANT_COLLECTION)
            except Exception:
                self.qdrant = None

    async def save_upload(self, file, uploaded_by: int) -> str:
        """
        Save incoming UploadFile to disk; return filepath.
        """
        ext = Path(file.filename).suffix or ""
        fname = f"{uuid4().hex}{ext}"
        dest = self.upload_dir / fname
        contents = await file.read()
        with open(dest, "wb") as f:
            f.write(contents)
        return str(dest)

    def ingest_file(self, filepath: str, uploaded_by: int):
        """
        Synchronous ingestion pipeline:
          - if image: OCR -> text
          - if text/pdf: extract text (pdf handled by future extension)
          - chunk text -> embeddings -> upsert to Qdrant
        """
        text = self._extract_text(filepath)
        if not text:
            return

        if RecursiveCharacterTextSplitter and self.qdrant:
            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
            docs = splitter.split_text(text)
            embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
            # Upsert to Qdrant via LangChain helper
            # For simplicity we add with minimal metadata
            try:
                self.qdrant.upsert(
                    points=[{"id": uuid4().hex, "vector": embeddings.embed_query(d), "payload": {"source": filepath}} for d in docs]
                )
            except Exception:
                # fallback: skip vector upsert if Qdrant not available
                pass

    def _extract_text(self, filepath: str) -> Optional[str]:
        """
        Very simple text extraction:
          - if .txt -> read
          - if image -> OCR if available
          - if pdf/docx -> TODO: extend
        """
        p = Path(filepath)
        if p.suffix.lower() in [".txt", ".md"]:
            return p.read_text(encoding="utf-8", errors="ignore")
        if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".tiff"] and pytesseract:
            img = Image.open(str(p))
            return pytesseract.image_to_string(img)
        # For pdf/docx you can integrate pypdf or docx2txt later
        return None
