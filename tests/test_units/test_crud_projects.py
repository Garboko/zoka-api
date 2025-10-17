import pytest
from sqlalchemy.orm import Session

from app.crud import projects as crud_projects
from app.schemas.projects import ProjectCreate, ProjectUpdate
from app.models.projects import Project


class TestProjectsCRUD:
    
    def test_get_project_by_id(self, db_session: Session):
        project_data = ProjectCreate(
            name="Test Project",
            description="Test Description",
            user_id="user123"
        )
        created_project = crud_projects.create(db_session, obj_in=project_data)
        
        found_project = crud_projects.get(db_session, id=created_project.id)
        
        assert found_project is not None
        assert found_project.id == created_project.id
        assert found_project.name == "Test Project"
        assert found_project.description == "Test Description"

    def test_get_project_by_id_not_found(self, db_session: Session):
        found_project = crud_projects.get(db_session, id="non_existent_id")
        
        assert found_project is None

    def test_get_projects_by_user_id(self, db_session: Session):
        user_id = "user123"
        project_data_1 = ProjectCreate(
            name="Project 1",
            description="Description 1",
            user_id=user_id
        )
        project_data_2 = ProjectCreate(
            name="Project 2", 
            description="Description 2",
            user_id=user_id
        )
        crud_projects.create(db_session, obj_in=project_data_1)
        crud_projects.create(db_session, obj_in=project_data_2)
        
        user_projects = crud_projects.get_by_user_id(db_session, user_id=user_id)
        
        assert len(user_projects) == 2
        assert all(project.user_id == user_id for project in user_projects)

    def test_get_projects_by_user_id_empty(self, db_session: Session):
        user_projects = crud_projects.get_by_user_id(db_session, user_id="no_projects_user")
        
        assert len(user_projects) == 0

    def test_create_project(self, db_session: Session):
        project_data = ProjectCreate(
            name="New Project",
            description="New Description",
            user_id="user123"
        )
        
        created_project = crud_projects.create(db_session, obj_in=project_data)
        
        assert created_project is not None
        assert created_project.id is not None
        assert created_project.name == "New Project"
        assert created_project.description == "New Description"
        assert created_project.user_id == "user123"
        assert created_project.is_active is True

    def test_update_project(self, db_session: Session):
        project_data = ProjectCreate(
            name="Original Project",
            description="Original Description",
            user_id="user123"
        )
        created_project = crud_projects.create(db_session, obj_in=project_data)
        
        update_data = ProjectUpdate(
            name="Updated Project",
            description="Updated Description",
            is_active=False
        )
        
        updated_project = crud_projects.update(db_session, db_obj=created_project, obj_in=update_data)
        
        assert updated_project.name == "Updated Project"
        assert updated_project.description == "Updated Description"
        assert updated_project.is_active is False
        assert updated_project.user_id == "user123"

    def test_update_project_partial(self, db_session: Session):
        project_data = ProjectCreate(
            name="Original Project",
            description="Original Description", 
            user_id="user123"
        )
        created_project = crud_projects.create(db_session, obj_in=project_data)
        
        update_data = ProjectUpdate(name="New Name Only")
        
        updated_project = crud_projects.update(db_session, db_obj=created_project, obj_in=update_data)
        
        assert updated_project.name == "New Name Only"
        assert updated_project.description == "Original Description"
        assert updated_project.is_active is True

    def test_delete_project(self, db_session: Session):
        project_data = ProjectCreate(
            name="Project to Delete",
            description="Delete Description",
            user_id="user123"
        )
        created_project = crud_projects.create(db_session, obj_in=project_data)
        
        deleted_project = crud_projects.delete(db_session, id=created_project.id)
        
        assert deleted_project is not None
        assert deleted_project.id == created_project.id
        
        found_project = crud_projects.get(db_session, id=created_project.id)
        assert found_project is None

    def test_delete_project_not_found(self, db_session: Session):
        result = crud_projects.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_projects(self, db_session: Session):
        user_id = "user123"
        projects_data = [
            ProjectCreate(name=f"Project {i}", description=f"Description {i}", user_id=user_id)
            for i in range(5)
        ]
        
        for project_data in projects_data:
            crud_projects.create(db_session, obj_in=project_data)
        
        projects = crud_projects.get_multi(db_session, skip=0, limit=10)
        
        assert len(projects) == 5
        assert all(isinstance(project, Project) for project in projects)

    def test_get_multi_projects_with_pagination(self, db_session: Session):
        user_id = "user123"
        projects_data = [
            ProjectCreate(name=f"Project {i}", description=f"Description {i}", user_id=user_id)
            for i in range(10)
        ]
        
        for project_data in projects_data:
            crud_projects.create(db_session, obj_in=project_data)
        
        first_page = crud_projects.get_multi(db_session, skip=0, limit=3)
        second_page = crud_projects.get_multi(db_session, skip=3, limit=3)
        
        assert len(first_page) == 3
        assert len(second_page) == 3
        
        first_ids = {project.id for project in first_page}
        second_ids = {project.id for project in second_page}
        assert first_ids.isdisjoint(second_ids)