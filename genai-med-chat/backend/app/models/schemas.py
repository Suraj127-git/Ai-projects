# backend/app/models/schemas.py
from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class MessageCreate(BaseModel):
    conv_id: Optional[int]
    sender: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
