import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    api_key_encrypted = Column(String, nullable=True)
    api_key_hint = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("MasterProfile", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="user")
