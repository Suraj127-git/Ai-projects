# backend/app/services/chat_service.py
import asyncio
from typing import Dict, Any

from app.adapters.model_adapter import ModelAdapter
from app.repos.mysql_repo import MySQLRepo
from app.core.config import settings

# Optional langchain imports (if installed)
try:
    from langchain.chains import RetrievalQA
    from langchain.vectorstores import Qdrant
    from langchain.embeddings import HuggingFaceEmbeddings
except Exception:
    Qdrant = None
    RetrievalQA = None
    HuggingFaceEmbeddings = None

class ChatService:
    def __init__(self):
        self.repo = MySQLRepo()
        self.model = ModelAdapter(backend=settings.MODEL_BACKEND)
        self._init_rag()

    def _init_rag(self):
        """
        Initialize vector store retriever (Qdrant) and RAG chain if langchain is available.
        If not installed, RAG will be disabled and service will fallback to model-only.
        """
        if Qdrant and HuggingFaceEmbeddings:
            try:
                emb = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
                self.vs = Qdrant(url=settings.QDRANT_URL, prefer_grpc=False, collection_name=settings.QDRANT_COLLECTION)
                retriever = self.vs.as_retriever(search_type="mmr", search_kwargs={"k": 3})
                self.rqa = RetrievalQA.from_chain_type(llm=self.model.llm, chain_type="stuff", retriever=retriever)
            except Exception as e:
                # fallback
                self.vs = None
                self.rqa = None
        else:
            self.vs = None
            self.rqa = None

    async def handle_query(self, user_id: int, text: str, modalities: Dict = None) -> Dict[str, Any]:
        """
        Main flow: 
          - optionally call retriever to get docs (RAG)
          - call model adapter to generate answer
          - persist the conversation
        """
        modalities = modalities or {}
        sources = []

        # 1) Retrieval if available
        if getattr(self, "rqa", None):
            try:
                # RetrievalQA.run is synchronous in many implementations, so run in thread
                loop = asyncio.get_event_loop()
                answer = await loop.run_in_executor(None, lambda: self.rqa.run(text))
                # LangChain RQA lacks explicit sources by default; for demo put placeholders
                sources = ["retrieved: doc1", "retrieved: doc2"]
            except Exception as e:
                answer = None
        else:
            answer = None

        # 2) If no RAG answer, fallback to model generation
        if not answer:
            # model_adapter.llm should accept a simple call interface
            try:
                # For blocking model calls run in executor
                loop = asyncio.get_event_loop()
                answer = await loop.run_in_executor(None, lambda: self.model.generate(text))
            except Exception as e:
                answer = "Sorry — model generation failed (check adapter)."

        # 3) Persist message to DB
        try:
            self.repo.create_message(conv_id=None, sender="user", content=text, metadata={"user_id": user_id})
            self.repo.create_message(conv_id=None, sender="bot", content=answer, metadata={"sources": sources})
        except Exception:
            # non-fatal for demo
            pass

        return {"answer": answer, "sources": sources}
