from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, JSON, Integer, Boolean, Text, Float, Index
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base
from sqlalchemy import Index

class APIToken(Base):
    __tablename__ = "api_tokens"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    token: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    permissions: Mapped[dict] = mapped_column(JSON, nullable=False) 
    rate_limit: Mapped[int] = mapped_column(Integer, default=1000)  
    expires_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    last_used: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    api_logs = relationship("APILog", back_populates="token", cascade="all, delete-orphan")

class APILog(Base):
    __tablename__ = "api_logs"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    token_id: Mapped[str] = mapped_column(String(36), ForeignKey("api_tokens.id", ondelete="CASCADE"), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(500), nullable=False) 
    method: Mapped[str] = mapped_column(String(10), nullable=False)  
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    response_time: Mapped[float] = mapped_column(Float)  
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    request_size: Mapped[Optional[int]] = mapped_column(Integer)  
    response_size: Mapped[Optional[int]] = mapped_column(Integer)  
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    token = relationship("APIToken", back_populates="api_logs")
    
    # Index 
    __table_args__ = (
        Index('idx_api_logs_created', 'created_at'),
        Index('idx_api_logs_token', 'token_id', 'created_at'),
    )