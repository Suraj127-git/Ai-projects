# genai-med-chat (local demo)
This is a local-first GenAI Medical Chat demo (FastAPI backend). Follow the infra/docker-compose.yml to start local services.

Steps:
1. Build files (you ran setup script).
2. Start infra: see infra/docker-compose.yml (edit envs as needed).
3. Run `python backend/scripts/init_db.py` to init DB.
4. Start backend: `uvicorn app.main:app --reload --port 8000` inside /backend
