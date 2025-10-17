from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.database.session import Base

class FormStatistic(Base):
    __tablename__ = "form_statistics"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"))
    total_submissions: Mapped[int] = mapped_column(Integer, default=0)
    last_submission: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    
    form: Mapped["Form"] = relationship(back_populates="form_statistics")