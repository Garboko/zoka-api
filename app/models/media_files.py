from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.database.session import Base

class MediaFile(Base):
    __tablename__ = "media_files"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    submission_id: Mapped[str] = mapped_column(String(36), ForeignKey("submissions.id", ondelete="CASCADE"), index=True)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    
    submission: Mapped["Submission"] = relationship(back_populates="media_files")