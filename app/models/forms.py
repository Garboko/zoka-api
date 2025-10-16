from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.session import Base

class Form(Base):
    __tablename__ = "forms"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("projects.id", ondelete="SET NULL"), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    original_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    converted_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    public_access: Mapped[bool] = mapped_column(Boolean, default=False)
    uuid_link: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user: Mapped["User"] = relationship(back_populates="forms")
    project: Mapped["Project"] = relationship(back_populates="forms")
    form_accesses: Mapped[list["FormAccess"]] = relationship(back_populates="form", cascade="all, delete-orphan")
    submissions: Mapped[list["Submission"]] = relationship(back_populates="form", cascade="all, delete-orphan")
    form_versions: Mapped[list["FormVersion"]] = relationship(back_populates="form", cascade="all, delete-orphan")
    form_statistics: Mapped[list["FormStatistic"]] = relationship(back_populates="form", cascade="all, delete-orphan")