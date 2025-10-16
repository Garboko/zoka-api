from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FormStatisticBase(BaseModel):
    form_id: str
    total_submissions: int = 0

class FormStatisticCreate(FormStatisticBase):
    pass

class FormStatisticUpdate(BaseModel):
    total_submissions: Optional[int] = None
    last_submission: Optional[datetime] = None

class FormStatisticResponse(FormStatisticBase):
    id: str
    last_submission: Optional[datetime] = None
    last_updated: datetime

    class Config:
        from_attributes = True