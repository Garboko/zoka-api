from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class EnumeratorBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    role: str = "enumerator"

class EnumeratorCreate(EnumeratorBase):
    user_id: str
    password: Optional[str] = None

class EnumeratorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None

class EnumeratorResponse(EnumeratorBase):
    id: str
    user_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)