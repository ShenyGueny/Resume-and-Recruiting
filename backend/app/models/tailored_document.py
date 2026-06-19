import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, Text, Enum, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from ..database import Base


class DocumentType(str, enum.Enum):
    RESUME = "resume"
    COVER_LETTER = "cover_letter"


class TailoredDocument(Base):
    __tablename__ = "tailored_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    content = Column(JSONB, nullable=True)
    content_text = Column(Text, nullable=True)
    ats_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="documents")
