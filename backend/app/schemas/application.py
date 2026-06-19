from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import Optional
from ..models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    company_name: str
    job_title: str
    job_description: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.SAVED
    applied_date: Optional[date] = None
    source_url: Optional[str] = None
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    applied_date: Optional[date] = None
    source_url: Optional[str] = None
    notes: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: UUID
    user_id: UUID
    company_name: str
    job_title: str
    job_description: Optional[str] = None
    status: ApplicationStatus
    applied_date: Optional[date] = None
    source_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
