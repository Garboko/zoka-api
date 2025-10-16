from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.email_verifications import EmailVerification
from app.schemas.email_verifications import EmailVerificationCreate, EmailVerificationUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[EmailVerification]:
    return db.query(EmailVerification).filter(EmailVerification.id == id).first()

def get_by_token(db: Session, token: str) -> Optional[EmailVerification]:
    return db.query(EmailVerification).filter(EmailVerification.token == token).first()

def get_by_user(db: Session, user_id: str) -> List[EmailVerification]:
    return db.query(EmailVerification).filter(EmailVerification.user_id == user_id).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[EmailVerification]:
    return db.query(EmailVerification).offset(skip).limit(limit).all()

def create(db: Session, obj_in: EmailVerificationCreate) -> EmailVerification:
    db_obj = EmailVerification(
        id=str(uuid4()),
        user_id=obj_in.user_id,
        token=obj_in.token,
        expires_at=obj_in.expires_at,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: EmailVerification, obj_in: EmailVerificationUpdate) -> EmailVerification:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[EmailVerification]:
    obj = db.query(EmailVerification).filter(EmailVerification.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj