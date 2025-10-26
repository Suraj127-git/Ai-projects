# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y build-essential git libxml2-dev libxslt1-dev default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create non-root user
RUN useradd -m appuser
USER appuser
WORKDIR /app

# Copy the entire app AFTER dependencies
COPY . /app

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
