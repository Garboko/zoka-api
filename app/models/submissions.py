from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.session import Base

class Submission(Base):
    __tablename__ = "submissions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"), index=True)
    enumerator_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("enumerators.id"), index=True, nullable=True)
    submission_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    validated: Mapped[bool] = mapped_column(Boolean, default=False)
    synced: Mapped[bool] = mapped_column(Boolean, default=True)
    
    form: Mapped["Form"] = relationship(back_populates="submissions")
    enumerator: Mapped["Enumerator"] = relationship(back_populates="submissions")
    media_files: Mapped[list["MediaFile"]] = relationship(back_populates="submission", cascade="all, delete-orphan")
    submission_reviews: Mapped[list["SubmissionReview"]] = relationship(back_populates="submission", cascade="all, delete-orphan")