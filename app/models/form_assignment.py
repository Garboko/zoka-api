from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base
import enum

class FormPermission(enum.Enum):
    view = "view"
    collect = "collect"
    manage = "manage"

class FormAssignment(Base):
    __tablename__ = "form_assignments"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    permissions: Mapped[FormPermission] = mapped_column(Enum(FormPermission), nullable=False)
    assigned_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    assigned_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    form = relationship("Form", back_populates="form_assignments")
    user = relationship("User", back_populates="form_assignments")
    assigner = relationship("User", foreign_keys=[assigned_by])
    __table_args__ = (
    UniqueConstraint('user_id', 'form_id', name='uq_user_form'),
    )