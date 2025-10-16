from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.audit_logs import AuditLog
from app.schemas.audit_logs import AuditLogCreate

def get(db: Session, id: int) -> Optional[AuditLog]:
    return db.query(AuditLog).filter(AuditLog.id == id).first()

def get_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
    return db.query(AuditLog).filter(AuditLog.user_id == user_id).offset(skip).limit(limit).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

def create(db: Session, obj_in: AuditLogCreate) -> AuditLog:
    db_obj = AuditLog(
        user_id=obj_in.user_id,
        enumerator_id=obj_in.enumerator_id,
        action=obj_in.action,
        table_name=obj_in.table_name,
        record_id=obj_in.record_id,
        description=obj_in.description,
        ip_address=obj_in.ip_address,
        user_agent=obj_in.user_agent,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj