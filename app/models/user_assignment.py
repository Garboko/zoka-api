from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database.session import Base
import enum

class ProjectRole(enum.Enum):
    viewer = "viewer"
    collector = "collector"
    manager = "manager"

class UserAssignment(Base):
    __tablename__ = "user_assignments"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[ProjectRole] = mapped_column(Enum(ProjectRole), nullable=False)
    assigned_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    assigned_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="user_assignments")
    project = relationship("Project", back_populates="user_assignments")
    assigner = relationship("User", foreign_keys=[assigned_by])