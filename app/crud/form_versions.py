from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.form_versions import FormVersion
from app.schemas.form_versions import FormVersionCreate, FormVersionUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[FormVersion]:
    return db.query(FormVersion).filter(FormVersion.id == id).first()

def get_by_form(db: Session, form_id: str) -> List[FormVersion]:
    return db.query(FormVersion).filter(FormVersion.form_id == form_id).order_by(FormVersion.version_number.desc()).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[FormVersion]:
    return db.query(FormVersion).offset(skip).limit(limit).all()

def create(db: Session, obj_in: FormVersionCreate) -> FormVersion:
    db_obj = FormVersion(
        id=str(uuid4()),
        form_id=obj_in.form_id,
        version_number=obj_in.version_number,
        xls_file_path=obj_in.xls_file_path,
        xml_file_path=obj_in.xml_file_path,
        changelog=obj_in.changelog,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: FormVersion, obj_in: FormVersionUpdate) -> FormVersion:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[FormVersion]:
    obj = db.query(FormVersion).filter(FormVersion.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj