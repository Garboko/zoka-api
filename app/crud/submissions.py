from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.submissions import Submission
from app.schemas.submissions import SubmissionCreate, SubmissionUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[Submission]:
    return db.query(Submission).filter(Submission.id == id).first()

def get_by_form(db: Session, form_id: str, skip: int = 0, limit: int = 100) -> List[Submission]:
    return db.query(Submission).filter(Submission.form_id == form_id).offset(skip).limit(limit).all()

def get_by_enumerator(db: Session, enumerator_id: str, skip: int = 0, limit: int = 100) -> List[Submission]:
    return db.query(Submission).filter(Submission.enumerator_id == enumerator_id).offset(skip).limit(limit).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Submission]:
    return db.query(Submission).offset(skip).limit(limit).all()

def create(db: Session, obj_in: SubmissionCreate) -> Submission:
    db_obj = Submission(
        id=str(uuid4()),
        form_id=obj_in.form_id,
        enumerator_id=obj_in.enumerator_id,
        submission_data=obj_in.submission_data,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Submission, obj_in: SubmissionUpdate) -> Submission:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[Submission]:
    obj = db.query(Submission).filter(Submission.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj