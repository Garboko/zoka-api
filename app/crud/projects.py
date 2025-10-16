from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.projects import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate
from uuid import uuid4

def get(db: Session, id: str) -> Optional[Project]:
    return db.query(Project).filter(Project.id == id).first()

def get_by_user_id(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Project]:
    return db.query(Project).filter(Project.user_id == user_id).offset(skip).limit(limit).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    return db.query(Project).offset(skip).limit(limit).all()

def create(db: Session, obj_in: ProjectCreate) -> Project:
    db_obj = Project(
        id=str(uuid4()),
        user_id=obj_in.user_id,
        name=obj_in.name,
        description=obj_in.description,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Project, obj_in: ProjectUpdate) -> Project:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[Project]:
    obj = db.query(Project).filter(Project.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj