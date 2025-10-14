from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base
import enum

class SyncStatusEnum(enum.Enum):
    synced = "synced"
    pending = "pending"
    error = "error"

class SyncStatus(Base):
    __tablename__ = "sync_status"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    last_sync: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    pending_submissions: Mapped[Optional[dict]] = mapped_column(JSON)
    status: Mapped[SyncStatusEnum] = mapped_column(Enum(SyncStatusEnum), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="sync_statuses")