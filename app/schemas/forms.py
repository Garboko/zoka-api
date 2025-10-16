from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FormBase(BaseModel):
    title: str
    description: Optional[str] = None
    public_access: bool = False

class FormCreate(FormBase):
    user_id: str
    project_id: Optional[str] = None
    original_file: Optional[str] = None
    converted_file: Optional[str] = None

class FormUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[str] = None
    original_file: Optional[str] = None
    converted_file: Optional[str] = None
    public_access: Optional[bool] = None
    version: Optional[int] = None

class FormResponse(FormBase):
    id: str
    user_id: str
    project_id: Optional[str] = None
    original_file: Optional[str] = None
    converted_file: Optional[str] = None
    uuid_link: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True