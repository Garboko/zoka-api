from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.form_versions import FormVersionCreate, FormVersionResponse, FormVersionUpdate
from app.crud import form_versions as crud_form_versions
from app.crud import forms as crud_forms
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=FormVersionResponse, status_code=status.HTTP_201_CREATED)
def create_form_version(
    form_version_in: FormVersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form = crud_forms.get(db, id=form_version_in.form_id)
    if not form or form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    form_version = crud_form_versions.create(db, obj_in=form_version_in)
    return form_version

@router.get("/form/{form_id}", response_model=List[FormVersionResponse])
def read_form_versions(
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
    
    versions = crud_form_versions.get_by_form(db, form_id=form_id)
    return versions

@router.get("/{version_id}", response_model=FormVersionResponse)
def read_form_version(
    version_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    version = crud_form_versions.get(db, id=version_id)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form version not found"
        )
    
    form = crud_forms.get(db, id=version.form_id)
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return version

@router.put("/{version_id}", response_model=FormVersionResponse)
def update_form_version(
    version_id: str,
    form_version_in: FormVersionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    version = crud_form_versions.get(db, id=version_id)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form version not found"
        )
    
    form = crud_forms.get(db, id=version.form_id)
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    version = crud_form_versions.update(db, db_obj=version, obj_in=form_version_in)
    return version

@router.delete("/{version_id}")
def delete_form_version(
    version_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    version = crud_form_versions.get(db, id=version_id)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form version not found"
        )
    
    form = crud_forms.get(db, id=version.form_id)
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    crud_form_versions.delete(db, id=version_id)
    return {"message": "Form version deleted successfully"}