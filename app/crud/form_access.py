from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.form_access import FormAccess
from app.schemas.form_access import FormAccessCreate, FormAccessUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[FormAccess]:
    return db.query(FormAccess).filter(FormAccess.id == id).first()

def get_by_enumerator_and_form(db: Session, enumerator_id: str, form_id: str) -> Optional[FormAccess]:
    return db.query(FormAccess).filter(
        FormAccess.enumerator_id == enumerator_id,
        FormAccess.form_id == form_id
    ).first()

def get_by_enumerator(db: Session, enumerator_id: str) -> List[FormAccess]:
    return db.query(FormAccess).filter(FormAccess.enumerator_id == enumerator_id).all()

def get_by_form(db: Session, form_id: str) -> List[FormAccess]:
    return db.query(FormAccess).filter(FormAccess.form_id == form_id).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[FormAccess]:
    return db.query(FormAccess).offset(skip).limit(limit).all()

def create(db: Session, obj_in: FormAccessCreate) -> FormAccess:
    db_obj = FormAccess(
        id=str(uuid4()),
        enumerator_id=obj_in.enumerator_id,
        form_id=obj_in.form_id,
        can_submit=obj_in.can_submit,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: FormAccess, obj_in: FormAccessUpdate) -> FormAccess:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[FormAccess]:
    obj = db.query(FormAccess).filter(FormAccess.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj