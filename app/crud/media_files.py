from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.media_files import MediaFile
from app.schemas.media_files import MediaFileCreate, MediaFileUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[MediaFile]:
    return db.query(MediaFile).filter(MediaFile.id == id).first()

def get_by_submission(db: Session, submission_id: str) -> List[MediaFile]:
    return db.query(MediaFile).filter(MediaFile.submission_id == submission_id).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[MediaFile]:
    return db.query(MediaFile).offset(skip).limit(limit).all()

def create(db: Session, obj_in: MediaFileCreate) -> MediaFile:
    db_obj = MediaFile(
        id=str(uuid4()),
        submission_id=obj_in.submission_id,
        file_path=obj_in.file_path,
        file_type=obj_in.file_type,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: MediaFile, obj_in: MediaFileUpdate) -> MediaFile:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[MediaFile]:
    obj = db.query(MediaFile).filter(MediaFile.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj