from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from typing import Optional, List
from app.database.session import Base
import enum

class ProjectType(enum.Enum):
    personal = "personal"
    organization = "organization"

class ProjectStatus(enum.Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    completed = "completed"

class ProjectVisibility(enum.Enum):
    private = "private"
    shared = "shared"
    public = "public"

class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    project_type: Mapped[ProjectType] = mapped_column(Enum(ProjectType), nullable=False)
    organization_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"))
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), nullable=False)
    visibility: Mapped[ProjectVisibility] = mapped_column(Enum(ProjectVisibility), default=ProjectVisibility.private)
    
    # Relationships
    report_templates = relationship("ReportTemplate", back_populates="project")
    webhooks = relationship("Webhook", back_populates="project")
    analytics_dashboards = relationship("AnalyticsDashboard", back_populates="project")
    organization = relationship("Organization", back_populates="projects")
    creator = relationship("User", back_populates="created_projects")
    forms = relationship("Form", back_populates="project")
    user_assignments = relationship("UserAssignment", back_populates="project")