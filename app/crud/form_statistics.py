from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.form_statistics import FormStatistic
from app.schemas.form_statistics import FormStatisticCreate, FormStatisticUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[FormStatistic]:
    return db.query(FormStatistic).filter(FormStatistic.id == id).first()

def get_by_form(db: Session, form_id: str) -> Optional[FormStatistic]:
    return db.query(FormStatistic).filter(FormStatistic.form_id == form_id).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[FormStatistic]:
    return db.query(FormStatistic).offset(skip).limit(limit).all()

def create(db: Session, obj_in: FormStatisticCreate) -> FormStatistic:
    db_obj = FormStatistic(
        id=str(uuid4()),
        form_id=obj_in.form_id,
        total_submissions=obj_in.total_submissions,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: FormStatistic, obj_in: FormStatisticUpdate) -> FormStatistic:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[FormStatistic]:
    obj = db.query(FormStatistic).filter(FormStatistic.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj