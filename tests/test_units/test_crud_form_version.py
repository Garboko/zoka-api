import pytest
from sqlalchemy.orm import Session

from app.crud import form_versions as crud_form_versions
from app.schemas.form_versions import FormVersionCreate, FormVersionUpdate
from app.models.form_versions import FormVersion


class TestFormVersionsCRUD:
    
    def test_get_form_version_by_id(self, db_session: Session):
        form_version_data = FormVersionCreate(
            form_id="form123",
            version_number=1,
            xls_file_path="/forms/form123/v1/form.xlsx",
            xml_file_path="/forms/form123/v1/form.xml",
            changelog="Initial version"
        )
        created_version = crud_form_versions.create(db_session, obj_in=form_version_data)
        
        found_version = crud_form_versions.get(db_session, id=created_version.id)
        
        assert found_version is not None
        assert found_version.id == created_version.id
        assert found_version.form_id == "form123"
        assert found_version.version_number == 1

    def test_get_form_version_by_id_not_found(self, db_session: Session):
        found_version = crud_form_versions.get(db_session, id="non_existent_id")
        
        assert found_version is None

    def test_get_form_versions_by_form(self, db_session: Session):
        form_id = "form123"
        form_version_data_1 = FormVersionCreate(
            form_id=form_id,
            version_number=1,
            changelog="Version 1"
        )
        form_version_data_2 = FormVersionCreate(
            form_id=form_id,
            version_number=2,
            changelog="Version 2"
        )
        crud_form_versions.create(db_session, obj_in=form_version_data_1)
        crud_form_versions.create(db_session, obj_in=form_version_data_2)
        
        form_versions = crud_form_versions.get_by_form(db_session, form_id=form_id)
        
        assert len(form_versions) == 2
        assert all(version.form_id == form_id for version in form_versions)
        assert form_versions[0].version_number == 2
        assert form_versions[1].version_number == 1

    def test_create_form_version(self, db_session: Session):
        form_version_data = FormVersionCreate(
            form_id="form123",
            version_number=3,
            xls_file_path="/forms/form123/v3/form.xlsx",
            xml_file_path="/forms/form123/v3/form.xml",
            changelog="Added new fields"
        )
        
        created_version = crud_form_versions.create(db_session, obj_in=form_version_data)
        
        assert created_version is not None
        assert created_version.id is not None
        assert created_version.form_id == "form123"
        assert created_version.version_number == 3
        assert created_version.xls_file_path == "/forms/form123/v3/form.xlsx"
        assert created_version.xml_file_path == "/forms/form123/v3/form.xml"
        assert created_version.changelog == "Added new fields"

    def test_create_form_version_minimal_data(self, db_session: Session):
        form_version_data = FormVersionCreate(
            form_id="form123",
            version_number=1
        )
        
        created_version = crud_form_versions.create(db_session, obj_in=form_version_data)
        
        assert created_version.version_number == 1
        assert created_version.form_id == "form123"
        assert created_version.xls_file_path is None
        assert created_version.xml_file_path is None
        assert created_version.changelog is None

    def test_update_form_version(self, db_session: Session):
        form_version_data = FormVersionCreate(
            form_id="form123",
            version_number=1,
            changelog="Original changelog"
        )
        created_version = crud_form_versions.create(db_session, obj_in=form_version_data)
        
        update_data = FormVersionUpdate(
            changelog="Updated changelog",
            xls_file_path="/new/path/form.xlsx",
            xml_file_path="/new/path/form.xml"
        )
        
        updated_version = crud_form_versions.update(db_session, db_obj=created_version, obj_in=update_data)
        
        assert updated_version.changelog == "Updated changelog"
        assert updated_version.xls_file_path == "/new/path/form.xlsx"
        assert updated_version.xml_file_path == "/new/path/form.xml"
        assert updated_version.form_id == "form123"
        assert updated_version.version_number == 1

    def test_update_form_version_partial(self, db_session: Session):
        form_version_data = FormVersionCreate(
            form_id="form123",
            version_number=1,
            changelog="Original changelog"
        )
        created_version = crud_form_versions.create(db_session, obj_in=form_version_data)
        
        update_data = FormVersionUpdate(changelog="New changelog only")
        
        updated_version = crud_form_versions.update(db_session, db_obj=created_version, obj_in=update_data)
        
        assert updated_version.changelog == "New changelog only"
        assert updated_version.form_id == "form123"
        assert updated_version.version_number == 1

    def test_delete_form_version(self, db_session: Session):
        form_version_data = FormVersionCreate(
            form_id="form123",
            version_number=1,
            changelog="Version to delete"
        )
        created_version = crud_form_versions.create(db_session, obj_in=form_version_data)
        
        deleted_version = crud_form_versions.delete(db_session, id=created_version.id)
        
        assert deleted_version is not None
        assert deleted_version.id == created_version.id
        
        found_version = crud_form_versions.get(db_session, id=created_version.id)
        assert found_version is None

    def test_delete_form_version_not_found(self, db_session: Session):
        result = crud_form_versions.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_form_versions(self, db_session: Session):
        form_versions_data = [
            FormVersionCreate(form_id=f"form{i}", version_number=i+1, changelog=f"Version {i+1}")
            for i in range(5)
        ]
        
        for form_version_data in form_versions_data:
            crud_form_versions.create(db_session, obj_in=form_version_data)
        
        form_versions = crud_form_versions.get_multi(db_session, skip=0, limit=10)
        
        assert len(form_versions) == 5
        assert all(isinstance(version, FormVersion) for version in form_versions)

    def test_get_multi_form_versions_with_pagination(self, db_session: Session):
        form_versions_data = [
            FormVersionCreate(form_id=f"form{i}", version_number=i+1, changelog=f"Version {i+1}")
            for i in range(10)
        ]
        
        for form_version_data in form_versions_data:
            crud_form_versions.create(db_session, obj_in=form_version_data)
        
        first_page = crud_form_versions.get_multi(db_session, skip=0, limit=4)
        second_page = crud_form_versions.get_multi(db_session, skip=4, limit=4)
        
        assert len(first_page) == 4
        assert len(second_page) == 4
        
        first_ids = {version.id for version in first_page}
        second_ids = {version.id for version in second_page}
        assert first_ids.isdisjoint(second_ids)