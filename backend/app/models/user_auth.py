"""User authentication model with password hashing."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
import uuid


class UserAuth(SQLModel, table=True):
    """User authentication table with password hashing."""

    __tablename__ = "user_auth"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
