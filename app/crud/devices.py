from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.devices import Device
from app.schemas.devices import DeviceCreate, DeviceUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[Device]:
    return db.query(Device).filter(Device.id == id).first()

def get_by_enumerator(db: Session, enumerator_id: str) -> List[Device]:
    return db.query(Device).filter(Device.enumerator_id == enumerator_id).all()

def get_by_device_uuid(db: Session, enumerator_id: str, device_uuid: str) -> Optional[Device]:
    return db.query(Device).filter(
        Device.enumerator_id == enumerator_id,
        Device.device_uuid == device_uuid
    ).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Device]:
    return db.query(Device).offset(skip).limit(limit).all()

def create(db: Session, obj_in: DeviceCreate) -> Device:
    db_obj = Device(
        id=str(uuid4()),
        enumerator_id=obj_in.enumerator_id,
        device_uuid=obj_in.device_uuid,
        model=obj_in.model,
        platform=obj_in.platform,
        app_version=obj_in.app_version,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Device, obj_in: DeviceUpdate) -> Device:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[Device]:
    obj = db.query(Device).filter(Device.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj