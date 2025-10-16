from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MediaFileBase(BaseModel):
    submission_id: str
    file_path: str
    file_type: Optional[str] = None

class MediaFileCreate(MediaFileBase):
    pass

class MediaFileUpdate(BaseModel):
    file_path: Optional[str] = None
    file_type: Optional[str] = None

class MediaFileResponse(MediaFileBase):
    id: str
    uploaded_at: datetime

    class Config:
        from_attributes = True