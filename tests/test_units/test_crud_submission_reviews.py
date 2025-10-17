import pytest
from sqlalchemy.orm import Session

from app.crud import submission_reviews as crud_submission_reviews
from app.schemas.submission_reviews import SubmissionReviewCreate, SubmissionReviewUpdate
from app.models.submission_reviews import SubmissionReview


class TestSubmissionReviewsCRUD:
    
    def test_get_submission_review_by_id(self, db_session: Session):
        review_data = SubmissionReviewCreate(
            submission_id="sub123",
            reviewer_id="user123",
            status="approved",
            comment="Good submission"
        )
        created_review = crud_submission_reviews.create(db_session, obj_in=review_data)
        
        found_review = crud_submission_reviews.get(db_session, id=created_review.id)
        
        assert found_review is not None
        assert found_review.id == created_review.id
        assert found_review.submission_id == "sub123"
        assert found_review.status == "approved"

    def test_get_submission_review_by_id_not_found(self, db_session: Session):
        found_review = crud_submission_reviews.get(db_session, id="non_existent_id")
        
        assert found_review is None

    def test_get_submission_reviews_by_submission(self, db_session: Session):
        submission_id = "sub123"
        review_data_1 = SubmissionReviewCreate(
            submission_id=submission_id,
            reviewer_id="user1",
            status="approved"
        )
        review_data_2 = SubmissionReviewCreate(
            submission_id=submission_id,
            reviewer_id="user2",
            status="rejected"
        )
        crud_submission_reviews.create(db_session, obj_in=review_data_1)
        crud_submission_reviews.create(db_session, obj_in=review_data_2)
        
        submission_reviews = crud_submission_reviews.get_by_submission(db_session, submission_id=submission_id)
        
        assert len(submission_reviews) == 2
        assert all(review.submission_id == submission_id for review in submission_reviews)

    def test_get_submission_reviews_by_reviewer(self, db_session: Session):
        reviewer_id = "user123"
        review_data_1 = SubmissionReviewCreate(
            submission_id="sub1",
            reviewer_id=reviewer_id,
            status="approved"
        )
        review_data_2 = SubmissionReviewCreate(
            submission_id="sub2",
            reviewer_id=reviewer_id,
            status="pending"
        )
        crud_submission_reviews.create(db_session, obj_in=review_data_1)
        crud_submission_reviews.create(db_session, obj_in=review_data_2)
        
        reviewer_reviews = crud_submission_reviews.get_by_reviewer(db_session, reviewer_id=reviewer_id)
        
        assert len(reviewer_reviews) == 2
        assert all(review.reviewer_id == reviewer_id for review in reviewer_reviews)

    def test_create_submission_review(self, db_session: Session):
        review_data = SubmissionReviewCreate(
            submission_id="sub123",
            reviewer_id="user123",
            status="approved",
            comment="Excellent work"
        )
        
        created_review = crud_submission_reviews.create(db_session, obj_in=review_data)
        
        assert created_review is not None
        assert created_review.id is not None
        assert created_review.submission_id == "sub123"
        assert created_review.reviewer_id == "user123"
        assert created_review.status == "approved"
        assert created_review.comment == "Excellent work"

    def test_create_submission_review_without_comment(self, db_session: Session):
        review_data = SubmissionReviewCreate(
            submission_id="sub123",
            reviewer_id="user123",
            status="pending"
        )
        
        created_review = crud_submission_reviews.create(db_session, obj_in=review_data)
        
        assert created_review.comment is None
        assert created_review.status == "pending"

    def test_create_submission_review_default_status(self, db_session: Session):
        review_data = SubmissionReviewCreate(
            submission_id="sub123",
            reviewer_id="user123"
        )
        
        created_review = crud_submission_reviews.create(db_session, obj_in=review_data)
        
        assert created_review.status == "pending"

    def test_update_submission_review(self, db_session: Session):
        review_data = SubmissionReviewCreate(
            submission_id="sub123",
            reviewer_id="user123",
            status="pending",
            comment="Initial comment"
        )
        created_review = crud_submission_reviews.create(db_session, obj_in=review_data)
        
        update_data = SubmissionReviewUpdate(
            status="approved",
            comment="Final approval"
        )
        
        updated_review = crud_submission_reviews.update(db_session, db_obj=created_review, obj_in=update_data)
        
        assert updated_review.status == "approved"
        assert updated_review.comment == "Final approval"
        assert updated_review.submission_id == "sub123"
        assert updated_review.reviewer_id == "user123"

    def test_update_submission_review_partial(self, db_session: Session):
        review_data = SubmissionReviewCreate(
            submission_id="sub123",
            reviewer_id="user123",
            status="pending",
            comment="Original comment"
        )
        created_review = crud_submission_reviews.create(db_session, obj_in=review_data)
        
        update_data = SubmissionReviewUpdate(status="rejected")
        
        updated_review = crud_submission_reviews.update(db_session, db_obj=created_review, obj_in=update_data)
        
        assert updated_review.status == "rejected"
        assert updated_review.comment == "Original comment"
        assert updated_review.submission_id == "sub123"

    def test_delete_submission_review(self, db_session: Session):
        review_data = SubmissionReviewCreate(
            submission_id="sub123",
            reviewer_id="user123",
            status="approved"
        )
        created_review = crud_submission_reviews.create(db_session, obj_in=review_data)
        
        deleted_review = crud_submission_reviews.delete(db_session, id=created_review.id)
        
        assert deleted_review is not None
        assert deleted_review.id == created_review.id
        
        found_review = crud_submission_reviews.get(db_session, id=created_review.id)
        assert found_review is None

    def test_delete_submission_review_not_found(self, db_session: Session):
        result = crud_submission_reviews.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_submission_reviews(self, db_session: Session):
        reviews_data = [
            SubmissionReviewCreate(submission_id=f"sub{i}", reviewer_id=f"user{i}", status="pending")
            for i in range(5)
        ]
        
        for review_data in reviews_data:
            crud_submission_reviews.create(db_session, obj_in=review_data)
        
        reviews = crud_submission_reviews.get_multi(db_session, skip=0, limit=10)
        
        assert len(reviews) == 5
        assert all(isinstance(review, SubmissionReview) for review in reviews)

    def test_get_multi_submission_reviews_with_pagination(self, db_session: Session):
        reviews_data = [
            SubmissionReviewCreate(submission_id=f"sub{i}", reviewer_id=f"user{i}", status="pending")
            for i in range(10)
        ]
        
        for review_data in reviews_data:
            crud_submission_reviews.create(db_session, obj_in=review_data)
        
        first_page = crud_submission_reviews.get_multi(db_session, skip=0, limit=4)
        second_page = crud_submission_reviews.get_multi(db_session, skip=4, limit=4)
        
        assert len(first_page) == 4
        assert len(second_page) == 4
        
        first_ids = {review.id for review in first_page}
        second_ids = {review.id for review in second_page}
        assert first_ids.isdisjoint(second_ids)