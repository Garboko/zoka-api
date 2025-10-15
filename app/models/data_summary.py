from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, JSON, Index
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base

class DataSummary(Base):
    __tablename__ = "data_summaries"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)  
    summary_type: Mapped[str] = mapped_column(String(50), nullable=False)  
    summary_data: Mapped[dict] = mapped_column(JSON, nullable=False)  
    filters: Mapped[Optional[dict]] = mapped_column(JSON)  
    calculated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True)) 
    
    # Relationships
    form = relationship("Form")
    
    # Index
    __table_args__ = (
        Index('idx_summary_form_field', 'form_id', 'field_name'),
        Index('idx_summary_type', 'summary_type'),
    )