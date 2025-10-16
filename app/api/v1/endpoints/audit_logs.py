from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.audit_logs import AuditLogCreate, AuditLogResponse
from app.crud import audit_logs as crud_audit_logs
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
def create_audit_log(
    audit_log_in: AuditLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    audit_log = crud_audit_logs.create(db, obj_in=audit_log_in)
    return audit_log

@router.get("/", response_model=List[AuditLogResponse])
def read_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    logs = crud_audit_logs.get_multi(db, skip=skip, limit=limit)
    return logs

@router.get("/user/{user_id}", response_model=List[AuditLogResponse])
def read_audit_logs_by_user(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    logs = crud_audit_logs.get_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return logs

@router.get("/{log_id}", response_model=AuditLogResponse)
def read_audit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    log = crud_audit_logs.get(db, id=log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log not found"
        )
    
    return log