from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Any, Optional


class TailorRequest(BaseModel):
    application_id: UUID


class ExtractionResult(BaseModel):
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    experience_level: str


class MatchResult(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    match_percentage: float


class GeneratedContent(BaseModel):
    tailored_bullets: list[str]
    summary: str


class ScoreBreakdown(BaseModel):
    skills: float
    experience: float
    education: float


class PipelineContent(BaseModel):
    extraction: ExtractionResult
    match: MatchResult
    generated: GeneratedContent
    score_breakdown: ScoreBreakdown


class TailoredDocumentResponse(BaseModel):
    id: UUID
    application_id: UUID
    document_type: str
    ats_score: Optional[float]
    content: Optional[dict[str, Any]]
    content_text: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
