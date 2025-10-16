from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.submission_reviews import SubmissionReview
from app.schemas.submission_reviews import SubmissionReviewCreate, SubmissionReviewUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[SubmissionReview]:
    return db.query(SubmissionReview).filter(SubmissionReview.id == id).first()

def get_by_submission(db: Session, submission_id: str) -> List[SubmissionReview]:
    return db.query(SubmissionReview).filter(SubmissionReview.submission_id == submission_id).all()

def get_by_reviewer(db: Session, reviewer_id: str, skip: int = 0, limit: int = 100) -> List[SubmissionReview]:
    return db.query(SubmissionReview).filter(SubmissionReview.reviewer_id == reviewer_id).offset(skip).limit(limit).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[SubmissionReview]:
    return db.query(SubmissionReview).offset(skip).limit(limit).all()

def create(db: Session, obj_in: SubmissionReviewCreate) -> SubmissionReview:
    db_obj = SubmissionReview(
        id=str(uuid4()),
        submission_id=obj_in.submission_id,
        reviewer_id=obj_in.reviewer_id,
        status=obj_in.status,
        comment=obj_in.comment,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: SubmissionReview, obj_in: SubmissionReviewUpdate) -> SubmissionReview:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[SubmissionReview]:
    obj = db.query(SubmissionReview).filter(SubmissionReview.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj