from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.forms import FormCreate, FormResponse, FormUpdate
from app.crud import forms as crud_forms
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=FormResponse, status_code=status.HTTP_201_CREATED)
def create_form(
    form_in: FormCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form_in.user_id = current_user.id
    form = crud_forms.create(db, obj_in=form_in)
    return form

@router.get("/", response_model=List[FormResponse])
def read_forms(
    skip: int = 0,
    limit: int = 100,
    project_id: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if project_id:
        forms = crud_forms.get_by_project_id(db, project_id=project_id, skip=skip, limit=limit)
    else:
        forms = crud_forms.get_by_user_id(db, user_id=current_user.id, skip=skip, limit=limit)
    return forms

@router.get("/{form_id}", response_model=FormResponse)
def read_form(
    form_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form = crud_forms.get(db, id=form_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return form

@router.put("/{form_id}", response_model=FormResponse)
def update_form(
    form_id: str,
    form_in: FormUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form = crud_forms.get(db, id=form_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    form = crud_forms.update(db, db_obj=form, obj_in=form_in)
    return form

@router.delete("/{form_id}")
def delete_form(
    form_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form = crud_forms.get(db, id=form_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    crud_forms.delete(db, id=form_id)
    return {"message": "Form deleted successfully"}