from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean, JSON, Integer
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base

class AnalyticsDashboard(Base):
    __tablename__ = "analytics_dashboards"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False)  
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project")
    creator = relationship("User")
    widgets = relationship("DashboardWidget", back_populates="dashboard", cascade="all, delete-orphan")

class DashboardWidget(Base):
    __tablename__ = "dashboard_widgets"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    dashboard_id: Mapped[str] = mapped_column(String(36), ForeignKey("analytics_dashboards.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    widget_type: Mapped[str] = mapped_column(String(50), nullable=False)  
    data_config: Mapped[dict] = mapped_column(JSON, nullable=False)
    display_config: Mapped[dict] = mapped_column(JSON, nullable=False) 
    position_x: Mapped[int] = mapped_column(Integer, default=0)
    position_y: Mapped[int] = mapped_column(Integer, default=0)
    width: Mapped[int] = mapped_column(Integer, default=4)
    height: Mapped[int] = mapped_column(Integer, default=3)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    dashboard = relationship("AnalyticsDashboard", back_populates="widgets")