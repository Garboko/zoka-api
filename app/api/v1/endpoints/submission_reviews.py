from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database.session import get_db
from app.schemas.submission_reviews import SubmissionReviewCreate, SubmissionReviewResponse, SubmissionReviewUpdate
from app.crud import submission_reviews as crud_submission_reviews
from app.crud import submissions as crud_submissions
from app.crud import forms as crud_forms
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=SubmissionReviewResponse, status_code=status.HTTP_201_CREATED)
def create_submission_review(
    review_in: SubmissionReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    submission = crud_submissions.get(db, id=review_in.submission_id)
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
    
    review_in.reviewer_id = current_user.id
    review = crud_submission_reviews.create(db, obj_in=review_in)
    return review

@router.get("/submission/{submission_id}", response_model=List[SubmissionReviewResponse])
def read_reviews_by_submission(
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
    
    reviews = crud_submission_reviews.get_by_submission(db, submission_id=submission_id)
    return reviews

@router.get("/{review_id}", response_model=SubmissionReviewResponse)
def read_submission_review(
    review_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    review = crud_submission_reviews.get(db, id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    submission = crud_submissions.get(db, id=review.submission_id)
    form = crud_forms.get(db, id=submission.form_id)
    
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return review

@router.put("/{review_id}", response_model=SubmissionReviewResponse)
def update_submission_review(
    review_id: str,
    review_in: SubmissionReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    review = crud_submission_reviews.get(db, id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.reviewer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if not review_in.reviewed_at:
        review_in.reviewed_at = datetime.now(timezone.utc)
    
    review = crud_submission_reviews.update(db, db_obj=review, obj_in=review_in)
    return review

@router.delete("/{review_id}")
def delete_submission_review(
    review_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    review = crud_submission_reviews.get(db, id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    submission = crud_submissions.get(db, id=review.submission_id)
    form = crud_forms.get(db, id=submission.form_id)
    
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    crud_submission_reviews.delete(db, id=review_id)
    return {"message": "Review deleted successfully"}