import pytest
from sqlalchemy.orm import Session

from app.crud import submissions as crud_submissions
from app.schemas.submissions import SubmissionCreate, SubmissionUpdate
from app.models.submissions import Submission


class TestSubmissionsCRUD:
    
    def test_get_submission_by_id(self, db_session: Session):
        submission_data = SubmissionCreate(
            form_id="form123",
            submission_data={"field1": "value1", "field2": "value2"},
            enumerator_id="enum123"
        )
        created_submission = crud_submissions.create(db_session, obj_in=submission_data)
        
        found_submission = crud_submissions.get(db_session, id=created_submission.id)
        
        assert found_submission is not None
        assert found_submission.id == created_submission.id
        assert found_submission.form_id == "form123"
        assert found_submission.submission_data == {"field1": "value1", "field2": "value2"}

    def test_get_submission_by_id_not_found(self, db_session: Session):
        found_submission = crud_submissions.get(db_session, id="non_existent_id")
        
        assert found_submission is None

    def test_get_submissions_by_form(self, db_session: Session):
        form_id = "form123"
        submission_data_1 = SubmissionCreate(
            form_id=form_id,
            submission_data={"data": "value1"},
            enumerator_id="enum123"
        )
        submission_data_2 = SubmissionCreate(
            form_id=form_id,
            submission_data={"data": "value2"},
            enumerator_id="enum456"
        )
        crud_submissions.create(db_session, obj_in=submission_data_1)
        crud_submissions.create(db_session, obj_in=submission_data_2)
        
        form_submissions = crud_submissions.get_by_form(db_session, form_id=form_id)
        
        assert len(form_submissions) == 2
        assert all(submission.form_id == form_id for submission in form_submissions)

    def test_get_submissions_by_enumerator(self, db_session: Session):
        enumerator_id = "enum123"
        submission_data_1 = SubmissionCreate(
            form_id="form1",
            submission_data={"data": "value1"},
            enumerator_id=enumerator_id
        )
        submission_data_2 = SubmissionCreate(
            form_id="form2",
            submission_data={"data": "value2"},
            enumerator_id=enumerator_id
        )
        crud_submissions.create(db_session, obj_in=submission_data_1)
        crud_submissions.create(db_session, obj_in=submission_data_2)
        
        enumerator_submissions = crud_submissions.get_by_enumerator(db_session, enumerator_id=enumerator_id)
        
        assert len(enumerator_submissions) == 2
        assert all(submission.enumerator_id == enumerator_id for submission in enumerator_submissions)

    def test_create_submission(self, db_session: Session):
        submission_data = SubmissionCreate(
            form_id="form123",
            submission_data={"name": "John", "age": 30, "city": "Paris"},
            enumerator_id="enum123"
        )
        
        created_submission = crud_submissions.create(db_session, obj_in=submission_data)
        
        assert created_submission is not None
        assert created_submission.id is not None
        assert created_submission.form_id == "form123"
        assert created_submission.submission_data == {"name": "John", "age": 30, "city": "Paris"}
        assert created_submission.enumerator_id == "enum123"
        assert created_submission.validated is False
        assert created_submission.synced == created_submission.synced

    def test_create_submission_without_enumerator(self, db_session: Session):
        submission_data = SubmissionCreate(
            form_id="form123",
            submission_data={"data": "anonymous"}
        )
        
        created_submission = crud_submissions.create(db_session, obj_in=submission_data)
        
        assert created_submission.enumerator_id is None
        assert created_submission.form_id == "form123"

    def test_update_submission(self, db_session: Session):
        submission_data = SubmissionCreate(
            form_id="form123",
            submission_data={"original": "data"},
            enumerator_id="enum123"
        )
        created_submission = crud_submissions.create(db_session, obj_in=submission_data)
        
        update_data = SubmissionUpdate(
            submission_data={"updated": "data"},
            validated=True,
            synced=True
        )
        
        updated_submission = crud_submissions.update(db_session, db_obj=created_submission, obj_in=update_data)
        
        assert updated_submission.submission_data == {"updated": "data"}
        assert updated_submission.validated is True
        assert updated_submission.synced is True
        assert updated_submission.form_id == "form123"

    def test_update_submission_partial(self, db_session: Session):
        submission_data = SubmissionCreate(
            form_id="form123",
            submission_data={"field1": "value1"},
            enumerator_id="enum123"
        )
        created_submission = crud_submissions.create(db_session, obj_in=submission_data)
        
        update_data = SubmissionUpdate(validated=True)
        
        updated_submission = crud_submissions.update(db_session, db_obj=created_submission, obj_in=update_data)
        
        assert updated_submission.validated is True
        assert updated_submission.submission_data == {"field1": "value1"}
        assert updated_submission.synced == updated_submission.synced

    def test_delete_submission(self, db_session: Session):
        submission_data = SubmissionCreate(
            form_id="form123",
            submission_data={"data": "to_delete"},
            enumerator_id="enum123"
        )
        created_submission = crud_submissions.create(db_session, obj_in=submission_data)
        
        deleted_submission = crud_submissions.delete(db_session, id=created_submission.id)
        
        assert deleted_submission is not None
        assert deleted_submission.id == created_submission.id
        
        found_submission = crud_submissions.get(db_session, id=created_submission.id)
        assert found_submission is None

    def test_delete_submission_not_found(self, db_session: Session):
        result = crud_submissions.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_submissions(self, db_session: Session):
        submissions_data = [
            SubmissionCreate(form_id=f"form{i}", submission_data={"data": f"value{i}"})
            for i in range(5)
        ]
        
        for submission_data in submissions_data:
            crud_submissions.create(db_session, obj_in=submission_data)
        
        submissions = crud_submissions.get_multi(db_session, skip=0, limit=10)
        
        assert len(submissions) == 5
        assert all(isinstance(submission, Submission) for submission in submissions)

    def test_get_multi_submissions_with_pagination(self, db_session: Session):
        submissions_data = [
            SubmissionCreate(form_id=f"form{i}", submission_data={"data": f"value{i}"})
            for i in range(10)
        ]
        
        for submission_data in submissions_data:
            crud_submissions.create(db_session, obj_in=submission_data)
        
        first_page = crud_submissions.get_multi(db_session, skip=0, limit=4)
        second_page = crud_submissions.get_multi(db_session, skip=4, limit=4)
        
        assert len(first_page) == 4
        assert len(second_page) == 4
        
        first_ids = {submission.id for submission in first_page}
        second_ids = {submission.id for submission in second_page}
        assert first_ids.isdisjoint(second_ids)