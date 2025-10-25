# backend/worker/celery_worker.py
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

@celery_app.task(bind=True)
def long_ingest_task(self, filepath: str, uploaded_by: int):
    """
    Example Celery task wrapper to call the ingest_service.
    In Docker compose the worker service uses this module.
    """
    from app.services.ingest_service import IngestService
    svc = IngestService()
    svc.ingest_file(filepath, uploaded_by)
    return {"status": "done", "file": filepath}
