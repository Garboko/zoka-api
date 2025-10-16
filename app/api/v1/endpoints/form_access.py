from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.form_access import FormAccessCreate, FormAccessResponse, FormAccessUpdate
from app.crud import form_access as crud_form_access
from app.crud import forms as crud_forms
from app.crud import enumerators as crud_enumerators
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=FormAccessResponse, status_code=status.HTTP_201_CREATED)
def create_form_access(
    form_access_in: FormAccessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form = crud_forms.get(db, id=form_access_in.form_id)
    if not form or form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    enumerator = crud_enumerators.get(db, id=form_access_in.enumerator_id)
    if not enumerator or enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Enumerator not found or not authorized"
        )
    
    existing_access = crud_form_access.get_by_enumerator_and_form(
        db, enumerator_id=form_access_in.enumerator_id, form_id=form_access_in.form_id
    )
    if existing_access:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access already granted"
        )
    
    form_access = crud_form_access.create(db, obj_in=form_access_in)
    return form_access

@router.get("/form/{form_id}", response_model=List[FormAccessResponse])
def read_form_accesses_by_form(
    form_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form = crud_forms.get(db, id=form_id)
    if not form or form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    accesses = crud_form_access.get_by_form(db, form_id=form_id)
    return accesses

@router.get("/enumerator/{enumerator_id}", response_model=List[FormAccessResponse])
def read_form_accesses_by_enumerator(
    enumerator_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enumerator = crud_enumerators.get(db, id=enumerator_id)
    if not enumerator or enumerator.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    accesses = crud_form_access.get_by_enumerator(db, enumerator_id=enumerator_id)
    return accesses

@router.put("/{form_access_id}", response_model=FormAccessResponse)
def update_form_access(
    form_access_id: str,
    form_access_in: FormAccessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form_access = crud_form_access.get(db, id=form_access_id)
    if not form_access:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form access not found"
        )
    
    form = crud_forms.get(db, id=form_access.form_id)
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    form_access = crud_form_access.update(db, db_obj=form_access, obj_in=form_access_in)
    return form_access

@router.delete("/{form_access_id}")
def delete_form_access(
    form_access_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form_access = crud_form_access.get(db, id=form_access_id)
    if not form_access:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form access not found"
        )
    
    form = crud_forms.get(db, id=form_access.form_id)
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    crud_form_access.delete(db, id=form_access_id)
    return {"message": "Form access deleted successfully"}