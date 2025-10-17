from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any

class SubmissionBase(BaseModel):
    form_id: str
    submission_data: Dict[str, Any]

class SubmissionCreate(SubmissionBase):
    enumerator_id: Optional[str] = None

class SubmissionUpdate(BaseModel):
    submission_data: Optional[Dict[str, Any]] = None
    validated: Optional[bool] = None
    synced: Optional[bool] = None

class SubmissionResponse(SubmissionBase):
    id: str
    enumerator_id: Optional[str] = None
    submitted_at: datetime
    validated: bool
    synced: bool
    
    model_config = ConfigDict(from_attributes=True)