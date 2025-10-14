from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base

class FormVersion(Base):
    __tablename__ = "form_versions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[str] = mapped_column(String(50), nullable=False)
    form_definition: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    form = relationship("Form", back_populates="form_versions")