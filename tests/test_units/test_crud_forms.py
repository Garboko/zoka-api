import pytest
from sqlalchemy.orm import Session

from app.crud import forms as crud_forms
from app.schemas.forms import FormCreate, FormUpdate
from app.models.forms import Form


class TestFormsCRUD:
    
    def test_get_form_by_id(self, db_session: Session):
        form_data = FormCreate(
            title="Test Form",
            description="Test Description",
            user_id="user123",
            project_id="project123"
        )
        created_form = crud_forms.create(db_session, obj_in=form_data)
        
        found_form = crud_forms.get(db_session, id=created_form.id)
        
        assert found_form is not None
        assert found_form.id == created_form.id
        assert found_form.title == "Test Form"
        assert found_form.description == "Test Description"

    def test_get_form_by_id_not_found(self, db_session: Session):
        found_form = crud_forms.get(db_session, id="non_existent_id")
        
        assert found_form is None

    def test_get_form_by_uuid_link(self, db_session: Session):
        form_data = FormCreate(
            title="Public Form",
            description="Public Description",
            user_id="user123",
            public_access=True
        )
        created_form = crud_forms.create(db_session, obj_in=form_data)
        
        found_form = crud_forms.get_by_uuid_link(db_session, uuid_link=created_form.uuid_link)
        
        assert found_form is not None
        assert found_form.id == created_form.id
        assert found_form.uuid_link == created_form.uuid_link

    def test_get_form_by_uuid_link_not_found(self, db_session: Session):
        found_form = crud_forms.get_by_uuid_link(db_session, uuid_link="invalid_uuid")
        
        assert found_form is None

    def test_get_forms_by_user_id(self, db_session: Session):
        user_id = "user123"
        form_data_1 = FormCreate(
            title="Form 1",
            description="Description 1",
            user_id=user_id
        )
        form_data_2 = FormCreate(
            title="Form 2",
            description="Description 2", 
            user_id=user_id
        )
        crud_forms.create(db_session, obj_in=form_data_1)
        crud_forms.create(db_session, obj_in=form_data_2)
        
        user_forms = crud_forms.get_by_user_id(db_session, user_id=user_id)
        
        assert len(user_forms) == 2
        assert all(form.user_id == user_id for form in user_forms)

    def test_get_forms_by_project_id(self, db_session: Session):
        project_id = "project123"
        form_data_1 = FormCreate(
            title="Form 1",
            description="Description 1",
            user_id="user123",
            project_id=project_id
        )
        form_data_2 = FormCreate(
            title="Form 2",
            description="Description 2",
            user_id="user123", 
            project_id=project_id
        )
        crud_forms.create(db_session, obj_in=form_data_1)
        crud_forms.create(db_session, obj_in=form_data_2)
        
        project_forms = crud_forms.get_by_project_id(db_session, project_id=project_id)
        
        assert len(project_forms) == 2
        assert all(form.project_id == project_id for form in project_forms)

    def test_create_form(self, db_session: Session):
        form_data = FormCreate(
            title="New Form",
            description="New Description",
            user_id="user123",
            project_id="project123",
            public_access=True
        )
        
        created_form = crud_forms.create(db_session, obj_in=form_data)
        
        assert created_form is not None
        assert created_form.id is not None
        assert created_form.title == "New Form"
        assert created_form.description == "New Description"
        assert created_form.user_id == "user123"
        assert created_form.project_id == "project123"
        assert created_form.public_access is True
        assert created_form.uuid_link is not None

    def test_create_form_without_public_access(self, db_session: Session):
        form_data = FormCreate(
            title="Private Form",
            description="Private Description",
            user_id="user123",
            public_access=False
        )
        
        created_form = crud_forms.create(db_session, obj_in=form_data)
        
        assert created_form.public_access is False
        assert created_form.uuid_link is None

    def test_update_form(self, db_session: Session):
        form_data = FormCreate(
            title="Original Form",
            description="Original Description",
            user_id="user123"
        )
        created_form = crud_forms.create(db_session, obj_in=form_data)
        
        update_data = FormUpdate(
            title="Updated Form",
            description="Updated Description",
            public_access=True
        )
        
        updated_form = crud_forms.update(db_session, db_obj=created_form, obj_in=update_data)
        
        assert updated_form.title == "Updated Form"
        assert updated_form.description == "Updated Description"
        assert updated_form.public_access is True
        assert updated_form.user_id == "user123"

    def test_update_form_partial(self, db_session: Session):
        form_data = FormCreate(
            title="Original Form",
            description="Original Description",
            user_id="user123"
        )
        created_form = crud_forms.create(db_session, obj_in=form_data)
        
        update_data = FormUpdate(title="New Title Only")
        
        updated_form = crud_forms.update(db_session, db_obj=created_form, obj_in=update_data)
        
        assert updated_form.title == "New Title Only"
        assert updated_form.description == "Original Description"
        assert updated_form.public_access is False

    def test_delete_form(self, db_session: Session):
        form_data = FormCreate(
            title="Form to Delete",
            description="Delete Description",
            user_id="user123"
        )
        created_form = crud_forms.create(db_session, obj_in=form_data)
        
        deleted_form = crud_forms.delete(db_session, id=created_form.id)
        
        assert deleted_form is not None
        assert deleted_form.id == created_form.id
        
        found_form = crud_forms.get(db_session, id=created_form.id)
        assert found_form is None

    def test_delete_form_not_found(self, db_session: Session):
        result = crud_forms.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_forms(self, db_session: Session):
        user_id = "user123"
        forms_data = [
            FormCreate(title=f"Form {i}", description=f"Description {i}", user_id=user_id)
            for i in range(5)
        ]
        
        for form_data in forms_data:
            crud_forms.create(db_session, obj_in=form_data)
        
        forms = crud_forms.get_multi(db_session, skip=0, limit=10)
        
        assert len(forms) == 5
        assert all(isinstance(form, Form) for form in forms)

    def test_get_multi_forms_with_pagination(self, db_session: Session):
        user_id = "user123"
        forms_data = [
            FormCreate(title=f"Form {i}", description=f"Description {i}", user_id=user_id)
            for i in range(10)
        ]
        
        for form_data in forms_data:
            crud_forms.create(db_session, obj_in=form_data)
        
        first_page = crud_forms.get_multi(db_session, skip=0, limit=4)
        second_page = crud_forms.get_multi(db_session, skip=4, limit=4)
        
        assert len(first_page) == 4
        assert len(second_page) == 4
        
        first_ids = {form.id for form in first_page}
        second_ids = {form.id for form in second_page}
        assert first_ids.isdisjoint(second_ids)