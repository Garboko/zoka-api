from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.media_files import MediaFileCreate, MediaFileResponse, MediaFileUpdate
from app.crud import media_files as crud_media_files
from app.crud import submissions as crud_submissions
from app.crud import forms as crud_forms
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=MediaFileResponse, status_code=status.HTTP_201_CREATED)
def create_media_file(
    media_file_in: MediaFileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    submission = crud_submissions.get(db, id=media_file_in.submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    media_file = crud_media_files.create(db, obj_in=media_file_in)
    return media_file

@router.get("/submission/{submission_id}", response_model=List[MediaFileResponse])
def read_media_files_by_submission(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    submission = crud_submissions.get(db, id=submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    form = crud_forms.get(db, id=submission.form_id)
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    media_files = crud_media_files.get_by_submission(db, submission_id=submission_id)
    return media_files

@router.get("/{media_file_id}", response_model=MediaFileResponse)
def read_media_file(
    media_file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    media_file = crud_media_files.get(db, id=media_file_id)
    if not media_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media file not found"
        )
    
    submission = crud_submissions.get(db, id=media_file.submission_id)
    form = crud_forms.get(db, id=submission.form_id)
    
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return media_file

@router.delete("/{media_file_id}")
def delete_media_file(
    media_file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    media_file = crud_media_files.get(db, id=media_file_id)
    if not media_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media file not found"
        )
    
    submission = crud_submissions.get(db, id=media_file.submission_id)
    form = crud_forms.get(db, id=submission.form_id)
    
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    crud_media_files.delete(db, id=media_file_id)
    return {"message": "Media file deleted successfully"}