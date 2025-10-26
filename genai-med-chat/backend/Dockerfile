# backend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (layer caching)
COPY requirements.txt /app/requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libxml2-dev \
    libxslt1-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create non-root user
RUN useradd -m appuser
USER appuser

# Set working dir (again as non-root)
WORKDIR /app

# Copy all backend files
COPY . /app

# Add Python path
ENV PYTHONPATH=/app

# Expose FastAPI port
EXPOSE 8000

# Correct CMD to point to the right module
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
