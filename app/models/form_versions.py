from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.session import Base

class FormVersion(Base):
    __tablename__ = "form_versions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"))
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    xls_file_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    xml_file_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    changelog: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    form: Mapped["Form"] = relationship(back_populates="form_versions")