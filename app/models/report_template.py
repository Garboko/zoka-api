from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum, JSON, Integer, Boolean
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base
import enum

class ReportFormat(enum.Enum):
    pdf = "pdf"
    excel = "excel"
    csv = "csv"
    word = "word"
    json = "json"

class ReportStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class ReportTemplate(Base):
    __tablename__ = "report_templates"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    format: Mapped[ReportFormat] = mapped_column(Enum(ReportFormat), nullable=False)
    template_config: Mapped[dict] = mapped_column(JSON, nullable=False)  
    default_filters: Mapped[Optional[dict]] = mapped_column(JSON)  
    include_media: Mapped[bool] = mapped_column(Boolean, default=False)
    language: Mapped[str] = mapped_column(String(10), default='fr')
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="report_templates")
    creator = relationship("User")
    report_jobs = relationship("ReportJob", back_populates="template", cascade="all, delete-orphan")

class ReportJob(Base):
    __tablename__ = "report_jobs"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    template_id: Mapped[str] = mapped_column(String(36), ForeignKey("report_templates.id", ondelete="CASCADE"), nullable=False)
    requested_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), nullable=False, default=ReportStatus.pending)
    filters: Mapped[dict] = mapped_column(JSON, nullable=False)  
    file_path: Mapped[Optional[str]] = mapped_column(String(500))  
    file_size: Mapped[Optional[int]] = mapped_column(Integer)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    progress: Mapped[int] = mapped_column(Integer, default=0)  
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    started_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    template = relationship("ReportTemplate", back_populates="report_jobs")
    requester = relationship("User")