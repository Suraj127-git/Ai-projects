#!/bin/bash
# setup_genai_project.sh
# This script creates folder and file structure for GenAI Medical Chat (local dev)

PROJECT_NAME="genai-med-chat"
BASE_DIR="$PWD/$PROJECT_NAME"

echo "Creating project: $PROJECT_NAME ..."
mkdir -p "$BASE_DIR"

# Backend structure
mkdir -p "$BASE_DIR/backend/app/api/v1"
mkdir -p "$BASE_DIR/backend/app/services"
mkdir -p "$BASE_DIR/backend/app/repos"
mkdir -p "$BASE_DIR/backend/app/models"
mkdir -p "$BASE_DIR/backend/app/core"
mkdir -p "$BASE_DIR/backend/app/adapters"
mkdir -p "$BASE_DIR/backend/worker"
mkdir -p "$BASE_DIR/backend/scripts"
mkdir -p "$BASE_DIR/backend/tests"
mkdir -p "$BASE_DIR/backend/data/uploads"

# Frontend structure
mkdir -p "$BASE_DIR/frontend/vite-react/src/components"

# Infrastructure & data
mkdir -p "$BASE_DIR/infra"
mkdir -p "$BASE_DIR/data/mysql"
mkdir -p "$BASE_DIR/data/qdrant"

# Backend files
touch "$BASE_DIR/backend/app/main.py"
touch "$BASE_DIR/backend/app/api/v1/chat.py"
touch "$BASE_DIR/backend/app/api/v1/ingest.py"
touch "$BASE_DIR/backend/app/services/chat_service.py"
touch "$BASE_DIR/backend/app/services/ingest_service.py"
touch "$BASE_DIR/backend/app/repos/mysql_repo.py"
touch "$BASE_DIR/backend/app/adapters/model_adapter.py"
touch "$BASE_DIR/backend/app/core/config.py"
touch "$BASE_DIR/backend/app/models/schemas.py"
touch "$BASE_DIR/backend/worker/celery_worker.py"
touch "$BASE_DIR/backend/scripts/ingest_documents.py"
touch "$BASE_DIR/backend/scripts/fine_tune.py"
touch "$BASE_DIR/backend/scripts/init_db.py"
touch "$BASE_DIR/backend/tests/test_chat_service.py"
touch "$BASE_DIR/backend/requirements.txt"
touch "$BASE_DIR/backend/Dockerfile"

# Frontend files
touch "$BASE_DIR/frontend/vite-react/package.json"
touch "$BASE_DIR/frontend/vite-react/vite.config.js"
touch "$BASE_DIR/frontend/vite-react/src/App.jsx"
touch "$BASE_DIR/frontend/vite-react/src/main.jsx"
touch "$BASE_DIR/frontend/vite-react/src/components/Chat.jsx"

# Infra files
touch "$BASE_DIR/infra/docker-compose.yml"
touch "$BASE_DIR/infra/README.md"

# SQL schema
touch "$BASE_DIR/backend/schemas.sql"

# Root docs
touch "$BASE_DIR/README.md"
touch "$BASE_DIR/.gitignore"

echo "✅ Folder and file structure created successfully in $BASE_DIR"
