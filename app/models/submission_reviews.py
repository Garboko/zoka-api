from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.session import Base

class SubmissionReview(Base):
    __tablename__ = "submission_reviews"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    submission_id: Mapped[str] = mapped_column(String(36), ForeignKey("submissions.id", ondelete="CASCADE"), index=True)
    reviewer_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    submission: Mapped["Submission"] = relationship(back_populates="submission_reviews")
    reviewer: Mapped["User"] = relationship(back_populates="submission_reviews")