from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from uuid import uuid4

def get(db: Session, id: str) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()

def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create(db: Session, obj_in: UserCreate) -> User:
    db_obj = User(
        id=str(uuid4()),
        email=obj_in.email,
        full_name=obj_in.full_name,
        password_hash=get_password_hash(obj_in.password),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: User, obj_in: UserUpdate) -> User:
    update_data = obj_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: str) -> Optional[User]:
    obj = db.query(User).filter(User.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user