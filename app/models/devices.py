from sqlalchemy import String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.session import Base

class Device(Base):
    __tablename__ = "devices"
    __table_args__ = (
        UniqueConstraint("enumerator_id", "device_uuid"),
    )
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    enumerator_id: Mapped[str] = mapped_column(String(36), ForeignKey("enumerators.id", ondelete="CASCADE"), index=True)
    device_uuid: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    platform: Mapped[str | None] = mapped_column(String(100), nullable=True)
    app_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_sync: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    enumerator: Mapped["Enumerator"] = relationship(back_populates="devices")