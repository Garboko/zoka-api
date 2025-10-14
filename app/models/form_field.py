from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Enum, Boolean, Integer, JSON
from sqlalchemy.sql import func
from typing import Optional
from app.database.session import Base
import enum

class FieldType(enum.Enum):
    text = "text"
    number = "number"
    date = "date"
    select_one = "select_one"
    select_multiple = "select_multiple"
    photo = "photo"
    audio = "audio"
    video = "video"
    gps = "gps"

class FormField(Base):
    __tablename__ = "form_fields"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)
    field_label: Mapped[str] = mapped_column(String(500), nullable=False)
    field_type: Mapped[FieldType] = mapped_column(Enum(FieldType), nullable=False)
    field_options: Mapped[Optional[dict]] = mapped_column(JSON)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False)
    validation_rules: Mapped[Optional[str]] = mapped_column(String(500))
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships
    form = relationship("Form", back_populates="form_fields")