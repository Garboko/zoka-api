import pytest
from sqlalchemy.orm import Session

from app.crud import enumerators as crud_enumerators
from app.schemas.enumerators import EnumeratorCreate, EnumeratorUpdate
from app.models.enumerators import Enumerator


class TestEnumeratorsCRUD:
    
    def test_get_enumerator_by_id(self, db_session: Session):
        enumerator_data = EnumeratorCreate(
            name="Test Enumerator",
            email="test@example.com",
            user_id="user123",
            password="password123"
        )
        created_enumerator = crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        found_enumerator = crud_enumerators.get(db_session, id=created_enumerator.id)
        
        assert found_enumerator is not None
        assert found_enumerator.id == created_enumerator.id
        assert found_enumerator.name == "Test Enumerator"
        assert found_enumerator.email == "test@example.com"

    def test_get_enumerator_by_id_not_found(self, db_session: Session):
        found_enumerator = crud_enumerators.get(db_session, id="non_existent_id")
        
        assert found_enumerator is None

    def test_get_enumerator_by_email(self, db_session: Session):
        enumerator_data = EnumeratorCreate(
            name="Test Enumerator",
            email="unique@example.com",
            user_id="user123",
            password="password123"
        )
        created_enumerator = crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        found_enumerator = crud_enumerators.get_by_email(db_session, email="unique@example.com")
        
        assert found_enumerator is not None
        assert found_enumerator.email == "unique@example.com"
        assert found_enumerator.id == created_enumerator.id

    def test_get_enumerator_by_email_not_found(self, db_session: Session):
        found_enumerator = crud_enumerators.get_by_email(db_session, email="nonexistent@example.com")
        
        assert found_enumerator is None

    def test_get_enumerators_by_user_id(self, db_session: Session):
        user_id = "user123"
        enumerator_data_1 = EnumeratorCreate(
            name="Enumerator 1",
            email="enum1@example.com",
            user_id=user_id,
            password="pass1"
        )
        enumerator_data_2 = EnumeratorCreate(
            name="Enumerator 2",
            email="enum2@example.com",
            user_id=user_id,
            password="pass2"
        )
        crud_enumerators.create(db_session, obj_in=enumerator_data_1)
        crud_enumerators.create(db_session, obj_in=enumerator_data_2)
        
        user_enumerators = crud_enumerators.get_by_user_id(db_session, user_id=user_id)
        
        assert len(user_enumerators) == 2
        assert all(enumerator.user_id == user_id for enumerator in user_enumerators)

    def test_create_enumerator(self, db_session: Session):
        enumerator_data = EnumeratorCreate(
            name="New Enumerator",
            email="new@example.com",
            user_id="user123",
            password="securepassword123"
        )
        
        created_enumerator = crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        assert created_enumerator is not None
        assert created_enumerator.id is not None
        assert created_enumerator.name == "New Enumerator"
        assert created_enumerator.email == "new@example.com"
        assert created_enumerator.user_id == "user123"
        assert created_enumerator.password_hash is not None
        assert created_enumerator.password_hash != "securepassword123"
        assert created_enumerator.is_active is True
        assert created_enumerator.role == "enumerator"

    def test_create_enumerator_without_password(self, db_session: Session):
        enumerator_data = EnumeratorCreate(
            name="No Password Enumerator",
            email="nopass@example.com",
            user_id="user123"
        )
        
        created_enumerator = crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        assert created_enumerator.password_hash is None
        assert created_enumerator.name == "No Password Enumerator"

    def test_create_enumerator_without_email(self, db_session: Session):
        enumerator_data = EnumeratorCreate(
            name="No Email Enumerator",
            user_id="user123",
            password="password123"
        )
        
        created_enumerator = crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        assert created_enumerator.email is None
        assert created_enumerator.name == "No Email Enumerator"

    def test_update_enumerator(self, db_session: Session):
        enumerator_data = EnumeratorCreate(
            name="Original Enumerator",
            email="original@example.com",
            user_id="user123",
            password="password123"
        )
        created_enumerator = crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        update_data = EnumeratorUpdate(
            name="Updated Enumerator",
            email="updated@example.com",
            is_active=False,
            role="supervisor"
        )
        
        updated_enumerator = crud_enumerators.update(db_session, db_obj=created_enumerator, obj_in=update_data)
        
        assert updated_enumerator.name == "Updated Enumerator"
        assert updated_enumerator.email == "updated@example.com"
        assert updated_enumerator.is_active is False
        assert updated_enumerator.role == "supervisor"
        assert updated_enumerator.user_id == "user123"

    def test_update_enumerator_password(self, db_session: Session):
        enumerator_data = EnumeratorCreate(
            name="Password Enumerator",
            email="password@example.com",
            user_id="user123",
            password="oldpassword"
        )
        created_enumerator = crud_enumerators.create(db_session, obj_in=enumerator_data)
        original_password_hash = created_enumerator.password_hash
        
        update_data = EnumeratorUpdate(password="newpassword")
        
        updated_enumerator = crud_enumerators.update(db_session, db_obj=created_enumerator, obj_in=update_data)
        
        assert updated_enumerator.password_hash != original_password_hash
        assert updated_enumerator.password_hash is not None

    def test_update_enumerator_partial(self, db_session: Session):
        enumerator_data = EnumeratorCreate(
            name="Original Enumerator",
            email="original@example.com",
            user_id="user123",
            password="password123"
        )
        created_enumerator = crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        update_data = EnumeratorUpdate(name="New Name Only")
        
        updated_enumerator = crud_enumerators.update(db_session, db_obj=created_enumerator, obj_in=update_data)
        
        assert updated_enumerator.name == "New Name Only"
        assert updated_enumerator.email == "original@example.com"
        assert updated_enumerator.is_active is True

    def test_delete_enumerator(self, db_session: Session):
        enumerator_data = EnumeratorCreate(
            name="Enumerator to Delete",
            email="delete@example.com",
            user_id="user123",
            password="password123"
        )
        created_enumerator = crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        deleted_enumerator = crud_enumerators.delete(db_session, id=created_enumerator.id)
        
        assert deleted_enumerator is not None
        assert deleted_enumerator.id == created_enumerator.id
        
        found_enumerator = crud_enumerators.get(db_session, id=created_enumerator.id)
        assert found_enumerator is None

    def test_delete_enumerator_not_found(self, db_session: Session):
        result = crud_enumerators.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_enumerators(self, db_session: Session):
        user_id = "user123"
        enumerators_data = [
            EnumeratorCreate(name=f"Enumerator {i}", email=f"enum{i}@example.com", user_id=user_id, password="pass")
            for i in range(5)
        ]
        
        for enumerator_data in enumerators_data:
            crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        enumerators = crud_enumerators.get_multi(db_session, skip=0, limit=10)
        
        assert len(enumerators) == 5
        assert all(isinstance(enumerator, Enumerator) for enumerator in enumerators)

    def test_get_multi_enumerators_with_pagination(self, db_session: Session):
        user_id = "user123"
        enumerators_data = [
            EnumeratorCreate(name=f"Enumerator {i}", email=f"enum{i}@example.com", user_id=user_id, password="pass")
            for i in range(10)
        ]
        
        for enumerator_data in enumerators_data:
            crud_enumerators.create(db_session, obj_in=enumerator_data)
        
        first_page = crud_enumerators.get_multi(db_session, skip=0, limit=4)
        second_page = crud_enumerators.get_multi(db_session, skip=4, limit=4)
        
        assert len(first_page) == 4
        assert len(second_page) == 4
        
        first_ids = {enumerator.id for enumerator in first_page}
        second_ids = {enumerator.id for enumerator in second_page}
        assert first_ids.isdisjoint(second_ids)