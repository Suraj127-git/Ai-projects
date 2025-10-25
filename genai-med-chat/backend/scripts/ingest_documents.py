# backend/scripts/ingest_documents.py
"""
Standalone script to ingest files from data/uploads folder.
Run: python backend/scripts/ingest_documents.py <filepath>
"""
import sys
from app.services.ingest_service import IngestService

def main():
    if len(sys.argv) < 2:
        print("Usage: python ingest_documents.py <filepath>")
        return
    path = sys.argv[1]
    svc = IngestService()
    svc.ingest_file(path, uploaded_by=0)
    print("Ingest finished for", path)

if __name__ == "__main__":
    main()
