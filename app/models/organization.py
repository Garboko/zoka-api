from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from typing import Optional, List
from app.database.session import Base

class Organization(Base):
    __tablename__ = "organizations"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_personal: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    owner = relationship("User", back_populates="owned_organizations")
    projects = relationship("Project", back_populates="organization")