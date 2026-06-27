from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.application import Application
from ..models.master_profile import MasterProfile
from ..models.tailored_document import TailoredDocument, DocumentType
from ..schemas.pipeline import TailorRequest, TailoredDocumentResponse
from ..services.auth_service import decrypt_api_key
from ..services.pipeline.orchestrator import run_pipeline
from ..dependencies import get_current_user

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/tailor", response_model=TailoredDocumentResponse)
def tailor(
    payload: TailorRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.api_key_encrypted:
        raise HTTPException(status_code=400, detail="No Anthropic API key on file. Add one via PUT /auth/api-key.")

    application = db.query(Application).filter(
        Application.id == payload.application_id,
        Application.user_id == current_user.id,
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if not application.job_description:
        raise HTTPException(status_code=400, detail="Application has no job description to analyze.")

    profile = db.query(MasterProfile).filter(MasterProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="No master profile found. Add one via PUT /profile.")

    api_key = decrypt_api_key(current_user.api_key_encrypted)
    profile_dict = {
        "experience": profile.experience or [],
        "education": profile.education or [],
        "skills": profile.skills or [],
    }

    try:
        ats_score, pipeline_content = run_pipeline(api_key, application.job_description, profile_dict)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI pipeline error: {str(e)}")

    content_text = (
        pipeline_content.generated.summary
        + "\n\n"
        + "\n".join(f"• {b}" for b in pipeline_content.generated.tailored_bullets)
    )

    doc = TailoredDocument(
        application_id=application.id,
        document_type=DocumentType.RESUME,
        content=pipeline_content.model_dump(),
        content_text=content_text,
        ats_score=ats_score,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/documents/{application_id}", response_model=List[TailoredDocumentResponse])
def list_documents(
    application_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id,
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return db.query(TailoredDocument).filter(
        TailoredDocument.application_id == application_id
    ).all()
