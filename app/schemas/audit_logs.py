from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AuditLogBase(BaseModel):
    action: str
    table_name: Optional[str] = None
    record_id: Optional[str] = None
    description: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    user_id: Optional[str] = None
    enumerator_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class AuditLogResponse(AuditLogBase):
    id: int
    user_id: Optional[str] = None
    enumerator_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)