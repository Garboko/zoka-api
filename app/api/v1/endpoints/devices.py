from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.devices import DeviceCreate, DeviceResponse, DeviceUpdate
from app.crud import devices as crud_devices
from app.crud import enumerators as crud_enumerators
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    device_in: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enumerator = crud_enumerators.get(db, id=device_in.enumerator_id)
    if not enumerator or enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    existing_device = crud_devices.get_by_device_uuid(
        db, enumerator_id=device_in.enumerator_id, device_uuid=device_in.device_uuid
    )
    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device already registered"
        )
    
    device = crud_devices.create(db, obj_in=device_in)
    return device

@router.get("/enumerator/{enumerator_id}", response_model=List[DeviceResponse])
def read_devices_by_enumerator(
    enumerator_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enumerator = crud_enumerators.get(db, id=enumerator_id)
    if not enumerator or enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    devices = crud_devices.get_by_enumerator(db, enumerator_id=enumerator_id)
    return devices

@router.get("/{device_id}", response_model=DeviceResponse)
def read_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    device = crud_devices.get(db, id=device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    enumerator = crud_enumerators.get(db, id=device.enumerator_id)
    if enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: str,
    device_in: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    device = crud_devices.get(db, id=device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    enumerator = crud_enumerators.get(db, id=device.enumerator_id)
    if enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    device = crud_devices.update(db, db_obj=device, obj_in=device_in)
    return device

@router.delete("/{device_id}")
def delete_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    device = crud_devices.get(db, id=device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    enumerator = crud_enumerators.get(db, id=device.enumerator_id)
    if enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    crud_devices.delete(db, id=device_id)
    return {"message": "Device deleted successfully"}