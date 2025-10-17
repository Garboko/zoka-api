import pytest
from sqlalchemy.orm import Session

from app.crud import users as crud_users
from app.schemas.users import UserCreate, UserUpdate
from app.models.users import User


class TestUsersCRUD:
    
    def test_get_user_by_id(self, db_session: Session):
        user_data = UserCreate(
            email="test@example.com",
            full_name="Test User", 
            password="testpassword123"
        )
        created_user = crud_users.create(db_session, obj_in=user_data)
        
        found_user = crud_users.get(db_session, id=created_user.id)
        
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == "test@example.com"
        assert found_user.full_name == "Test User"

    def test_get_user_by_id_not_found(self, db_session: Session):
        found_user = crud_users.get(db_session, id="non_existent_id")
        
        assert found_user is None

    def test_get_user_by_email(self, db_session: Session):
        user_data = UserCreate(
            email="unique@example.com",
            full_name="Test User",
            password="testpassword123"
        )
        created_user = crud_users.create(db_session, obj_in=user_data)
        
        found_user = crud_users.get_by_email(db_session, email="unique@example.com")
        
        assert found_user is not None
        assert found_user.email == "unique@example.com"
        assert found_user.id == created_user.id

    def test_get_user_by_email_not_found(self, db_session: Session):
        found_user = crud_users.get_by_email(db_session, email="nonexistent@example.com")
        
        assert found_user is None

    def test_create_user(self, db_session: Session):
        user_data = UserCreate(
            email="newuser@example.com",
            full_name="New User",
            password="securepassword123"
        )
        
        created_user = crud_users.create(db_session, obj_in=user_data)
        
        assert created_user is not None
        assert created_user.id is not None
        assert created_user.email == "newuser@example.com"
        assert created_user.full_name == "New User"
        assert created_user.password_hash is not None
        assert created_user.password_hash != "securepassword123"
        assert hasattr(created_user, 'is_active')
        assert hasattr(created_user, 'email_verified')

    def test_create_user_duplicate_email(self, db_session: Session):
        user_data = UserCreate(
            email="duplicate@example.com",
            full_name="First User",
            password="password123"
        )
        crud_users.create(db_session, obj_in=user_data)
        
        duplicate_data = UserCreate(
            email="duplicate@example.com",
            full_name="Second User",
            password="password456"
        )
        
        with pytest.raises(Exception):
            crud_users.create(db_session, obj_in=duplicate_data)

    def test_update_user(self, db_session: Session):
        user_data = UserCreate(
            email="update@example.com",
            full_name="Original Name",
            password="password123"
        )
        created_user = crud_users.create(db_session, obj_in=user_data)
        
        update_data = UserUpdate(
            full_name="Updated Name",
            is_active=False
        )
        
        updated_user = crud_users.update(db_session, db_obj=created_user, obj_in=update_data)
        
        assert updated_user.full_name == "Updated Name"
        assert updated_user.is_active is False
        assert updated_user.email == "update@example.com"

    def test_update_user_password(self, db_session: Session):
        user_data = UserCreate(
            email="password@example.com",
            full_name="Password User",
            password="oldpassword"
        )
        created_user = crud_users.create(db_session, obj_in=user_data)
        original_password_hash = created_user.password_hash
        
        update_data = UserUpdate(password="newpassword")
        
        updated_user = crud_users.update(db_session, db_obj=created_user, obj_in=update_data)
        
        assert updated_user.password_hash != original_password_hash
        assert updated_user.password_hash is not None

    def test_delete_user(self, db_session: Session):
        user_data = UserCreate(
            email="delete@example.com",
            full_name="User to Delete",
            password="password123"
        )
        created_user = crud_users.create(db_session, obj_in=user_data)
        
        deleted_user = crud_users.delete(db_session, id=created_user.id)
        
        assert deleted_user is not None
        assert deleted_user.id == created_user.id
        
        found_user = crud_users.get(db_session, id=created_user.id)
        assert found_user is None

    def test_delete_user_not_found(self, db_session: Session):
        result = crud_users.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_authenticate_user_success(self, db_session: Session):
        user_data = UserCreate(
            email="auth@example.com",
            full_name="Auth User",
            password="correctpassword"
        )
        crud_users.create(db_session, obj_in=user_data)
        
        authenticated_user = crud_users.authenticate(
            db_session, email="auth@example.com", password="correctpassword"
        )
        
        assert authenticated_user is not None
        assert authenticated_user.email == "auth@example.com"

    def test_authenticate_user_wrong_password(self, db_session: Session):
        user_data = UserCreate(
            email="auth@example.com",
            full_name="Auth User", 
            password="correctpassword"
        )
        crud_users.create(db_session, obj_in=user_data)
        
        authenticated_user = crud_users.authenticate(
            db_session, email="auth@example.com", password="wrongpassword"
        )
        
        assert authenticated_user is None

    def test_authenticate_user_not_found(self, db_session: Session):
        authenticated_user = crud_users.authenticate(
            db_session, email="nonexistent@example.com", password="anypassword"
        )
        
        assert authenticated_user is None

    def test_get_multi_users(self, db_session: Session):
        users_data = [
            UserCreate(email=f"user{i}@example.com", full_name=f"User {i}", password="pass")
            for i in range(5)
        ]
        
        for user_data in users_data:
            crud_users.create(db_session, obj_in=user_data)
        
        users = crud_users.get_multi(db_session, skip=0, limit=10)
        
        assert len(users) == 5
        assert all(isinstance(user, User) for user in users)

    def test_get_multi_users_with_pagination(self, db_session: Session):
        users_data = [
            UserCreate(email=f"user{i}@example.com", full_name=f"User {i}", password="pass")
            for i in range(10)
        ]
        
        for user_data in users_data:
            crud_users.create(db_session, obj_in=user_data)
        
        first_page = crud_users.get_multi(db_session, skip=0, limit=5)
        second_page = crud_users.get_multi(db_session, skip=5, limit=5)
        
        assert len(first_page) == 5
        assert len(second_page) == 5
        
        first_ids = {user.id for user in first_page}
        second_ids = {user.id for user in second_page}
        assert first_ids.isdisjoint(second_ids)