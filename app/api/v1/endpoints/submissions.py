from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.submissions import SubmissionCreate, SubmissionResponse, SubmissionUpdate
from app.crud import submissions as crud_submissions
from app.crud import forms as crud_forms
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def create_submission(
    submission_in: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    form = crud_forms.get(db, id=submission_in.form_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    
    submission = crud_submissions.create(db, obj_in=submission_in)
    return submission

@router.get("/", response_model=List[SubmissionResponse])
def read_submissions(
    skip: int = 0,
    limit: int = 100,
    form_id: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if form_id:
        form = crud_forms.get(db, id=form_id)
        if not form or form.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        submissions = crud_submissions.get_by_form(db, form_id=form_id, skip=skip, limit=limit)
    else:
        submissions = crud_submissions.get_multi(db, skip=skip, limit=limit)
    
    return submissions

@router.get("/{submission_id}", response_model=SubmissionResponse)
def read_submission(
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
    
    return submission

@router.put("/{submission_id}", response_model=SubmissionResponse)
def update_submission(
    submission_id: str,
    submission_in: SubmissionUpdate,
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
    
    submission = crud_submissions.update(db, db_obj=submission, obj_in=submission_in)
    return submission

@router.delete("/{submission_id}")
def delete_submission(
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
    
    crud_submissions.delete(db, id=submission_id)
    return {"message": "Submission deleted successfully"}