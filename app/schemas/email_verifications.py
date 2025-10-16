from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmailVerificationBase(BaseModel):
    user_id: str
    token: str
    expires_at: datetime

class EmailVerificationCreate(EmailVerificationBase):
    pass

class EmailVerificationUpdate(BaseModel):
    used: Optional[bool] = None

class EmailVerificationResponse(EmailVerificationBase):
    id: str
    used: bool
    created_at: datetime

    class Config:
        from_attributes = True