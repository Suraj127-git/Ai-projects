# backend/app/repos/mysql_repo.py
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text, JSON, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.core.config import settings

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(255), unique=True),
    Column("email", String(255), unique=True),
    Column("password_hash", String(255)),
    Column("role", String(50)),
    Column("created_at", TIMESTAMP, server_default=func.current_timestamp())
)

conversations = Table(
    "conversations", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("title", String(255)),
    Column("created_at", TIMESTAMP, server_default=func.current_timestamp())
)

messages = Table(
    "messages", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("conv_id", Integer),
    Column("sender", Enum("user", "bot")),
    Column("content", Text),
    Column("metadata", JSON),
    Column("created_at", TIMESTAMP, server_default=func.current_timestamp())
)

# Simple synchronous engine for demo. In production use async engine + session
engine = create_engine(settings.MYSQL_DSN, echo=False, future=True)

class MySQLRepo:
    def __init__(self):
        # Create tables if not exist (simple demo)
        metadata.create_all(engine)

    def create_user(self, username: str, email: str, password_hash: str, role: str = "user"):
        with engine.begin() as conn:
            res = conn.execute(users.insert().values(username=username, email=email, password_hash=password_hash, role=role))
            return res.inserted_primary_key[0]

    def create_message(self, conv_id, sender, content, metadata: dict = None):
        with engine.begin() as conn:
            res = conn.execute(messages.insert().values(conv_id=conv_id, sender=sender, content=content, metadata=metadata))
            return res.inserted_primary_key[0]
