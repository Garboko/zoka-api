from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum, Boolean, JSON
from sqlalchemy.sql import func
from typing import Optional, List
from app.database.session import Base
import enum

class FormStatus(enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

class Form(Base):
    __tablename__ = "forms"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    form_definition: Mapped[dict] = mapped_column(JSON, nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    status: Mapped[FormStatus] = mapped_column(Enum(FormStatus), nullable=False)
    allow_offline: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    project = relationship("Project", back_populates="forms")
    creator = relationship("User")
    form_versions = relationship("FormVersion", back_populates="form")
    submissions = relationship("Submission", back_populates="form")
    form_fields = relationship("FormField", back_populates="form")
    form_assignments = relationship("FormAssignment", back_populates="form")