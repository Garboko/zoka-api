from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.enumerators import Enumerator
from app.schemas.enumerators import EnumeratorCreate, EnumeratorUpdate
from app.core.security import get_password_hash
from uuid import uuid4

def get(db: Session, id: str) -> Optional[Enumerator]:
    return db.query(Enumerator).filter(Enumerator.id == id).first()

def get_by_user_id(db: Session, user_id: str) -> List[Enumerator]:
    return db.query(Enumerator).filter(Enumerator.user_id == user_id).all()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Enumerator]:
    return db.query(Enumerator).offset(skip).limit(limit).all()

def create(db: Session, obj_in: EnumeratorCreate) -> Enumerator:
    password_hash = None
    if obj_in.password:
        password_hash = get_password_hash(obj_in.password)
    
    db_obj = Enumerator(
        id=str(uuid4()),
        user_id=obj_in.user_id,
        name=obj_in.name,
        email=obj_in.email,
        password_hash=password_hash,
        role=obj_in.role,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Enumerator, obj_in: EnumeratorUpdate) -> Enumerator:
    update_data = obj_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[Enumerator]:
    obj = db.query(Enumerator).filter(Enumerator.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj