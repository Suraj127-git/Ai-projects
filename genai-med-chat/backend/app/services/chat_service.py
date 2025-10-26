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
            except Exception:
                self.vs = None
                self.rqa = None
        else:
            self.vs = None
            self.rqa = None

    async def handle_query(self, user_id: int, text: str, modalities: Dict = None) -> Dict[str, Any]:
        """
        Extended flow:
          - Ensure a conversation exists (create one)
          - Record user message as node
          - Run retrieval (if available) and record retrieval nodes
          - Generate answer using model and record generation node
          - Link nodes: user -> retrieval(s) -> generation
        """
        modalities = modalities or {}
        sources = []

        # 0) Create conversation (simple title)
        try:
            conv_id = self.repo.create_conversation(user_id=user_id, title=(text[:50] + "..."))
        except Exception:
            conv_id = None

        # Create LangGraph service
        from app.services.langgraph_service import LangGraphService
        lg = LangGraphService()

        # 1) Record user node
        user_node_id = None
        if conv_id is not None:
            user_node_id = lg.record_node(conv_id=conv_id, node_type="user", content=text, metadata={"user_id": user_id})

        # 2) Retrieval if available
        retrieval_node_ids = []
        retrieval_texts = []
        if getattr(self, "rqa", None):
            try:
                loop = asyncio.get_event_loop()
                rqa_output = await loop.run_in_executor(None, lambda: self.rqa.run(text))
                # For demo: get top documents if retriever exists
                try:
                    retriever = self.vs.as_retriever(search_type="mmr", search_kwargs={"k": 3})
                    docs = retriever.get_relevant_documents(text)
                except Exception:
                    docs = []
                for d in docs:
                    content_snippet = (d.page_content[:400] if hasattr(d, "page_content") else str(d))
                    nid = lg.record_node(conv_id=conv_id, node_type="retrieval", content=content_snippet, metadata={"source": getattr(d, "metadata", {})})
                    retrieval_node_ids.append(nid)
                    retrieval_texts.append(content_snippet)
                    sources.append(getattr(d, "metadata", {}))
            except Exception:
                pass

        # 3) Generation step
        answer = None
        try:
            loop = asyncio.get_event_loop()
            answer = await loop.run_in_executor(None, lambda: self.model.generate(text))
        except Exception:
            answer = "Sorry — model generation failed."

        # Record generation node
        gen_node_id = None
        if conv_id is not None:
            gen_node_id = lg.record_node(conv_id=conv_id, node_type="generation", content=answer, metadata={"sources": sources})

        # 4) Create edges: user -> retrieval(s), retrieval(s) -> generation, user -> generation
        try:
            if conv_id is not None and user_node_id:
                if gen_node_id:
                    lg.record_edge(conv_id=conv_id, from_node=user_node_id, to_node=gen_node_id, relation="asked_for")
                for r_nid in retrieval_node_ids:
                    lg.record_edge(conv_id=conv_id, from_node=user_node_id, to_node=r_nid, relation="retrieved")
                    if gen_node_id:
                        lg.record_edge(conv_id=conv_id, from_node=r_nid, to_node=gen_node_id, relation="informed")
        except Exception:
            pass

        # 5) Persist messages to DB
        try:
            self.repo.create_message(conv_id=conv_id, sender="user", content=text, metadata={"user_id": user_id})
            self.repo.create_message(conv_id=conv_id, sender="bot", content=answer, metadata={"sources": sources})
        except Exception:
            pass

        return {"answer": answer, "sources": sources, "conv_id": conv_id}
