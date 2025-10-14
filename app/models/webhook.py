from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base

class Webhook(Base):
    __tablename__ = "webhooks"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    events: Mapped[dict] = mapped_column(JSON, nullable=False)  
    secret: Mapped[Optional[str]] = mapped_column(String(100)) 
    config: Mapped[dict] = mapped_column(JSON, nullable=False) 
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project")
    creator = relationship("User")
    webhook_logs = relationship("WebhookLog", back_populates="webhook", cascade="all, delete-orphan")

class WebhookLog(Base):
    __tablename__ = "webhook_logs"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    webhook_id: Mapped[str] = mapped_column(String(36), ForeignKey("webhooks.id", ondelete="CASCADE"), nullable=False)
    event: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    response_status: Mapped[Optional[int]] = mapped_column(Integer)
    response_body: Mapped[Optional[str]] = mapped_column(Text)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    attempted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    next_retry_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    webhook = relationship("Webhook", back_populates="webhook_logs")
    
    # Index 
    __table_args__ = (
        Index('idx_webhook_logs_attempted', 'attempted_at'),
        Index('idx_webhook_logs_retry', 'next_retry_at'),
    )