from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SubmissionReviewBase(BaseModel):
    submission_id: str
    status: str = "pending"
    comment: Optional[str] = None

class SubmissionReviewCreate(SubmissionReviewBase):
    reviewer_id: Optional[str] = None

class SubmissionReviewUpdate(BaseModel):
    status: Optional[str] = None
    comment: Optional[str] = None
    reviewed_at: Optional[datetime] = None

class SubmissionReviewResponse(SubmissionReviewBase):
    id: str
    reviewer_id: Optional[str] = None
    reviewed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)