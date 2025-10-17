from sqlalchemy import String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.database.session import Base

class FormAccess(Base):
    __tablename__ = "form_access"
    __table_args__ = (
        UniqueConstraint("enumerator_id", "form_id"),
    )
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    enumerator_id: Mapped[str] = mapped_column(String(36), ForeignKey("enumerators.id", ondelete="CASCADE"), index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"), index=True)
    can_submit: Mapped[bool] = mapped_column(Boolean, default=True)
    granted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    
    enumerator: Mapped["Enumerator"] = relationship(back_populates="form_accesses")
    form: Mapped["Form"] = relationship(back_populates="form_accesses")