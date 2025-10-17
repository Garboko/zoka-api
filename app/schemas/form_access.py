from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class FormAccessBase(BaseModel):
    enumerator_id: str
    form_id: str
    can_submit: bool = True

class FormAccessCreate(FormAccessBase):
    pass

class FormAccessUpdate(BaseModel):
    can_submit: Optional[bool] = None

class FormAccessResponse(FormAccessBase):
    id: str
    granted_at: datetime

    model_config = ConfigDict(from_attributes=True)