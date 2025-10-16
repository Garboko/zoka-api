from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.forms import Form
from app.schemas.forms import FormCreate, FormUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[Form]:
    return db.query(Form).filter(Form.id == id).first()

def get_by_uuid_link(db: Session, uuid_link: str) -> Optional[Form]:
    return db.query(Form).filter(Form.uuid_link == uuid_link).first()

def get_by_user_id(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Form]:
    return db.query(Form).filter(Form.user_id == user_id).offset(skip).limit(limit).all()

def get_by_project_id(db: Session, project_id: str, skip: int = 0, limit: int = 100) -> List[Form]:
    return db.query(Form).filter(Form.project_id == project_id).offset(skip).limit(limit).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Form]:
    return db.query(Form).offset(skip).limit(limit).all()

def create(db: Session, obj_in: FormCreate) -> Form:
    db_obj = Form(
        id=str(uuid4()),
        user_id=obj_in.user_id,
        project_id=obj_in.project_id,
        title=obj_in.title,
        description=obj_in.description,
        original_file=obj_in.original_file,
        converted_file=obj_in.converted_file,
        public_access=obj_in.public_access,
        uuid_link=str(uuid4()) if obj_in.public_access else None,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Form, obj_in: FormUpdate) -> Form:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[Form]:
    obj = db.query(Form).filter(Form.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj