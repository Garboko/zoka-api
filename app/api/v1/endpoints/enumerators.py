from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.enumerators import EnumeratorCreate, EnumeratorResponse, EnumeratorUpdate
from app.crud import enumerators as crud_enumerators
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=EnumeratorResponse, status_code=status.HTTP_201_CREATED)
def create_enumerator(
    enumerator_in: EnumeratorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enumerator_in.user_id = current_user.id
    enumerator = crud_enumerators.create(db, obj_in=enumerator_in)
    return enumerator

@router.get("/", response_model=List[EnumeratorResponse])
def read_enumerators(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enumerators = crud_enumerators.get_by_user_id(db, user_id=current_user.id)
    return enumerators

@router.get("/{enumerator_id}", response_model=EnumeratorResponse)
def read_enumerator(
    enumerator_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enumerator = crud_enumerators.get(db, id=enumerator_id)
    if not enumerator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enumerator not found"
        )
    
    if enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return enumerator

@router.put("/{enumerator_id}", response_model=EnumeratorResponse)
def update_enumerator(
    enumerator_id: str,
    enumerator_in: EnumeratorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enumerator = crud_enumerators.get(db, id=enumerator_id)
    if not enumerator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enumerator not found"
        )
    
    if enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    enumerator = crud_enumerators.update(db, db_obj=enumerator, obj_in=enumerator_in)
    return enumerator

@router.delete("/{enumerator_id}")
def delete_enumerator(
    enumerator_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enumerator = crud_enumerators.get(db, id=enumerator_id)
    if not enumerator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enumerator not found"
        )
    
    if enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    crud_enumerators.delete(db, id=enumerator_id)
    return {"message": "Enumerator deleted successfully"}