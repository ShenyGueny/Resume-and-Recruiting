from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    api_key_hint: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ApiKeyUpdate(BaseModel):
    api_key: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
