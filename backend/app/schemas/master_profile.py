from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Any, Optional


class MasterProfileCreate(BaseModel):
    experience: list[dict[str, Any]] = []
    education: list[dict[str, Any]] = []
    skills: list[str] = []


class MasterProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    experience: list[dict[str, Any]]
    education: list[dict[str, Any]]
    skills: list[str]
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
