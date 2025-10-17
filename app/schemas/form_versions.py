from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class FormVersionBase(BaseModel):
    form_id: str
    version_number: int
    changelog: Optional[str] = None

class FormVersionCreate(FormVersionBase):
    xls_file_path: Optional[str] = None
    xml_file_path: Optional[str] = None

class FormVersionUpdate(BaseModel):
    changelog: Optional[str] = None
    xls_file_path: Optional[str] = None
    xml_file_path: Optional[str] = None

class FormVersionResponse(FormVersionBase):
    id: str
    xls_file_path: Optional[str] = None
    xml_file_path: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)