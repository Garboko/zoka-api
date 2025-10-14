from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from typing import Optional, List
from app.database.session import Base
import enum

class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"
    enumerator = "enumerator"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    owned_organizations = relationship("Organization", back_populates="owner")
    created_projects = relationship("Project", back_populates="creator")
    user_assignments = relationship("UserAssignment", back_populates="user")
    form_assignments = relationship("FormAssignment", back_populates="user")
    submissions = relationship("Submission", back_populates="submitter")
    audit_logs = relationship("AuditLog", back_populates="user")
    sync_statuses = relationship("SyncStatus", back_populates="user")