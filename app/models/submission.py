from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Enum, JSON, DECIMAL
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base
import enum

class SubmissionStatus(enum.Enum):
    draft = "draft"
    submitted = "submitted"
    validated = "validated"
    rejected = "rejected"

class Submission(Base):
    __tablename__ = "submissions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    submitted_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    submission_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    submitted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    synced_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[SubmissionStatus] = mapped_column(Enum(SubmissionStatus), nullable=False)
    device_id: Mapped[Optional[str]] = mapped_column(String(255))
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    latitude: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 8))
    longitude: Mapped[Optional[float]] = mapped_column(DECIMAL(11, 8))
    
    # Relationships
    form = relationship("Form", back_populates="submissions")
    submitter = relationship("User", back_populates="submissions")
    media_files = relationship("MediaFile", back_populates="submission")
    __table_args__ = (
        Index('idx_submission_form_status', 'form_id', 'status'),
        Index('idx_submission_submitter', 'submitted_by'),
        Index('idx_submission_date', 'submitted_at'),
        Index('idx_submission_location', 'latitude', 'longitude'),  
    )