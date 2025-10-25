# backend/app/adapters/model_adapter.py
import os
from typing import Any

from app.core.config import settings

# Try to import transformers locally; otherwise provide a dumb fallback
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
except Exception:
    pipeline = None

import requests
import json
import time

class BaseLLM:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

class HFLocalAdapter(BaseLLM):
    def __init__(self, model_name: str):
        if pipeline:
            # text-generation pipeline; for causal models adjust params
            self.gen = pipeline("text-generation", model=model_name, max_length=256)
        else:
            self.gen = None
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        if self.gen:
            out = self.gen(prompt, max_length=256, do_sample=True)
            # pipeline returns list of dicts
            return out[0]["generated_text"] if isinstance(out, list) else str(out)
        else:
            # fallback simple echo
            return f"[hf-local mock] {prompt[:200]}"

class OllamaAdapter(BaseLLM):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "ollama-model"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        # Ollama REST simple call (if hosted locally). Example POST /api/generate
        url = f"{self.base_url}/api/generate"
        payload = {"model": self.model, "prompt": prompt}
        try:
            r = requests.post(url, json=payload, timeout=15)
            r.raise_for_status()
            j = r.json()
            # adjust according to Ollama response format
            return j.get("text", str(j))
        except Exception as e:
            return f"[ollama mock/fail] {str(e)}"

class ModelAdapter:
    def __init__(self, backend: str = "hf", hf_model: str = None, ollama_url: str = None, ollama_model: str = None):
        backend = backend.lower() if backend else "hf"
        if backend == "ollama":
            self.adapter = OllamaAdapter(base_url=ollama_url or settings.OLLAMA_URL, model=ollama_model or settings.OLLAMA_MODEL)
        else:
            self.adapter = HFLocalAdapter(model_name=hf_model or settings.HF_MODEL)

    @property
    def llm(self):
        # For LangChain integration you might wrap this into an object that LangChain expects.
        return self

    def generate(self, prompt: str) -> str:
        return self.adapter.generate(prompt)
