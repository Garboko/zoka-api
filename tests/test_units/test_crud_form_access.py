import pytest
from sqlalchemy.orm import Session

from app.crud import form_access as crud_form_access
from app.schemas.form_access import FormAccessCreate, FormAccessUpdate
from app.models.form_access import FormAccess


class TestFormAccessCRUD:
    
    def test_get_form_access_by_id(self, db_session: Session):
        form_access_data = FormAccessCreate(
            enumerator_id="enum123",
            form_id="form123",
            can_submit=True
        )
        created_access = crud_form_access.create(db_session, obj_in=form_access_data)
        
        found_access = crud_form_access.get(db_session, id=created_access.id)
        
        assert found_access is not None
        assert found_access.id == created_access.id
        assert found_access.enumerator_id == "enum123"
        assert found_access.form_id == "form123"

    def test_get_form_access_by_id_not_found(self, db_session: Session):
        found_access = crud_form_access.get(db_session, id="non_existent_id")
        
        assert found_access is None

    def test_get_form_access_by_enumerator_and_form(self, db_session: Session):
        form_access_data = FormAccessCreate(
            enumerator_id="enum123",
            form_id="form123",
            can_submit=True
        )
        created_access = crud_form_access.create(db_session, obj_in=form_access_data)
        
        found_access = crud_form_access.get_by_enumerator_and_form(
            db_session, enumerator_id="enum123", form_id="form123"
        )
        
        assert found_access is not None
        assert found_access.id == created_access.id
        assert found_access.enumerator_id == "enum123"
        assert found_access.form_id == "form123"

    def test_get_form_access_by_enumerator_and_form_not_found(self, db_session: Session):
        found_access = crud_form_access.get_by_enumerator_and_form(
            db_session, enumerator_id="enum123", form_id="form456"
        )
        
        assert found_access is None

    def test_get_form_accesses_by_enumerator(self, db_session: Session):
        enumerator_id = "enum123"
        form_access_data_1 = FormAccessCreate(
            enumerator_id=enumerator_id,
            form_id="form1",
            can_submit=True
        )
        form_access_data_2 = FormAccessCreate(
            enumerator_id=enumerator_id,
            form_id="form2",
            can_submit=False
        )
        crud_form_access.create(db_session, obj_in=form_access_data_1)
        crud_form_access.create(db_session, obj_in=form_access_data_2)
        
        enumerator_accesses = crud_form_access.get_by_enumerator(db_session, enumerator_id=enumerator_id)
        
        assert len(enumerator_accesses) == 2
        assert all(access.enumerator_id == enumerator_id for access in enumerator_accesses)

    def test_get_form_accesses_by_form(self, db_session: Session):
        form_id = "form123"
        form_access_data_1 = FormAccessCreate(
            enumerator_id="enum1",
            form_id=form_id,
            can_submit=True
        )
        form_access_data_2 = FormAccessCreate(
            enumerator_id="enum2",
            form_id=form_id,
            can_submit=False
        )
        crud_form_access.create(db_session, obj_in=form_access_data_1)
        crud_form_access.create(db_session, obj_in=form_access_data_2)
        
        form_accesses = crud_form_access.get_by_form(db_session, form_id=form_id)
        
        assert len(form_accesses) == 2
        assert all(access.form_id == form_id for access in form_accesses)

    def test_create_form_access(self, db_session: Session):
        form_access_data = FormAccessCreate(
            enumerator_id="enum123",
            form_id="form123",
            can_submit=True
        )
        
        created_access = crud_form_access.create(db_session, obj_in=form_access_data)
        
        assert created_access is not None
        assert created_access.id is not None
        assert created_access.enumerator_id == "enum123"
        assert created_access.form_id == "form123"
        assert created_access.can_submit is True

    def test_create_form_access_without_submit_permission(self, db_session: Session):
        form_access_data = FormAccessCreate(
            enumerator_id="enum123",
            form_id="form123",
            can_submit=False
        )
        
        created_access = crud_form_access.create(db_session, obj_in=form_access_data)
        
        assert created_access.can_submit is False

    def test_update_form_access(self, db_session: Session):
        form_access_data = FormAccessCreate(
            enumerator_id="enum123",
            form_id="form123",
            can_submit=True
        )
        created_access = crud_form_access.create(db_session, obj_in=form_access_data)
        
        update_data = FormAccessUpdate(can_submit=False)
        
        updated_access = crud_form_access.update(db_session, db_obj=created_access, obj_in=update_data)
        
        assert updated_access.can_submit is False
        assert updated_access.enumerator_id == "enum123"
        assert updated_access.form_id == "form123"

    def test_delete_form_access(self, db_session: Session):
        form_access_data = FormAccessCreate(
            enumerator_id="enum123",
            form_id="form123",
            can_submit=True
        )
        created_access = crud_form_access.create(db_session, obj_in=form_access_data)
        
        deleted_access = crud_form_access.delete(db_session, id=created_access.id)
        
        assert deleted_access is not None
        assert deleted_access.id == created_access.id
        
        found_access = crud_form_access.get(db_session, id=created_access.id)
        assert found_access is None

    def test_delete_form_access_not_found(self, db_session: Session):
        result = crud_form_access.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_form_accesses(self, db_session: Session):
        form_accesses_data = [
            FormAccessCreate(enumerator_id=f"enum{i}", form_id=f"form{i}", can_submit=True)
            for i in range(5)
        ]
        
        for form_access_data in form_accesses_data:
            crud_form_access.create(db_session, obj_in=form_access_data)
        
        form_accesses = crud_form_access.get_multi(db_session, skip=0, limit=10)
        
        assert len(form_accesses) == 5
        assert all(isinstance(access, FormAccess) for access in form_accesses)

    def test_get_multi_form_accesses_with_pagination(self, db_session: Session):
        form_accesses_data = [
            FormAccessCreate(enumerator_id=f"enum{i}", form_id=f"form{i}", can_submit=True)
            for i in range(10)
        ]
        
        for form_access_data in form_accesses_data:
            crud_form_access.create(db_session, obj_in=form_access_data)
        
        first_page = crud_form_access.get_multi(db_session, skip=0, limit=4)
        second_page = crud_form_access.get_multi(db_session, skip=4, limit=4)
        
        assert len(first_page) == 4
        assert len(second_page) == 4
        
        first_ids = {access.id for access in first_page}
        second_ids = {access.id for access in second_page}
        assert first_ids.isdisjoint(second_ids)