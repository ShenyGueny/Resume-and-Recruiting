from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.master_profile import MasterProfile
from ..schemas.master_profile import MasterProfileCreate, MasterProfileResponse
from ..dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=MasterProfileResponse)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(MasterProfile).filter(MasterProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("", response_model=MasterProfileResponse)
def upsert_profile(
    payload: MasterProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(MasterProfile).filter(MasterProfile.user_id == current_user.id).first()
    if profile:
        profile.experience = payload.experience
        profile.education = payload.education
        profile.skills = payload.skills
    else:
        profile = MasterProfile(user_id=current_user.id, **payload.model_dump())
        db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
