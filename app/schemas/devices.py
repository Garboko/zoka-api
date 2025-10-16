from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeviceBase(BaseModel):
    enumerator_id: str
    device_uuid: str
    model: Optional[str] = None
    platform: Optional[str] = None
    app_version: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    model: Optional[str] = None
    platform: Optional[str] = None
    app_version: Optional[str] = None
    last_sync: Optional[datetime] = None
    is_active: Optional[bool] = None

class DeviceResponse(DeviceBase):
    id: str
    last_sync: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True