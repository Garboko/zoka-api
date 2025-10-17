import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from app.crud import email_verifications as crud_email_verifications
from app.schemas.email_verifications import EmailVerificationCreate, EmailVerificationUpdate
from app.models.email_verifications import EmailVerification


class TestEmailVerificationsCRUD:
    
    def test_get_email_verification_by_id(self, db_session: Session):
        verification_data = EmailVerificationCreate(
            user_id="user123",
            token="token123",
            expires_at=datetime(2024, 12, 31, 23, 59, 59)
        )
        created_verification = crud_email_verifications.create(db_session, obj_in=verification_data)
        
        found_verification = crud_email_verifications.get(db_session, id=created_verification.id)
        
        assert found_verification is not None
        assert found_verification.id == created_verification.id
        assert found_verification.user_id == "user123"
        assert found_verification.token == "token123"

    def test_get_email_verification_by_id_not_found(self, db_session: Session):
        found_verification = crud_email_verifications.get(db_session, id="non_existent_id")
        
        assert found_verification is None

    def test_get_email_verification_by_token(self, db_session: Session):
        verification_data = EmailVerificationCreate(
            user_id="user123",
            token="unique_token_123",
            expires_at=datetime(2024, 12, 31, 23, 59, 59)
        )
        created_verification = crud_email_verifications.create(db_session, obj_in=verification_data)
        
        found_verification = crud_email_verifications.get_by_token(db_session, token="unique_token_123")
        
        assert found_verification is not None
        assert found_verification.token == "unique_token_123"
        assert found_verification.id == created_verification.id

    def test_get_email_verification_by_token_not_found(self, db_session: Session):
        found_verification = crud_email_verifications.get_by_token(db_session, token="invalid_token")
        
        assert found_verification is None

    def test_get_email_verifications_by_user(self, db_session: Session):
        user_id = "user123"
        verification_data_1 = EmailVerificationCreate(
            user_id=user_id,
            token="token1",
            expires_at=datetime(2024, 12, 31, 23, 59, 59)
        )
        verification_data_2 = EmailVerificationCreate(
            user_id=user_id,
            token="token2",
            expires_at=datetime(2024, 12, 31, 23, 59, 59)
        )
        crud_email_verifications.create(db_session, obj_in=verification_data_1)
        crud_email_verifications.create(db_session, obj_in=verification_data_2)
        
        user_verifications = crud_email_verifications.get_by_user(db_session, user_id=user_id)
        
        assert len(user_verifications) == 2
        assert all(verification.user_id == user_id for verification in user_verifications)

    def test_create_email_verification(self, db_session: Session):
        expires_at = datetime(2024, 12, 31, 23, 59, 59)
        verification_data = EmailVerificationCreate(
            user_id="user123",
            token="new_token_123",
            expires_at=expires_at
        )
        
        created_verification = crud_email_verifications.create(db_session, obj_in=verification_data)
        
        assert created_verification is not None
        assert created_verification.id is not None
        assert created_verification.user_id == "user123"
        assert created_verification.token == "new_token_123"
        assert created_verification.expires_at == expires_at
        assert created_verification.used is False

    def test_update_email_verification(self, db_session: Session):
        verification_data = EmailVerificationCreate(
            user_id="user123",
            token="token123",
            expires_at=datetime(2024, 12, 31, 23, 59, 59)
        )
        created_verification = crud_email_verifications.create(db_session, obj_in=verification_data)
        
        update_data = EmailVerificationUpdate(used=True)
        
        updated_verification = crud_email_verifications.update(db_session, db_obj=created_verification, obj_in=update_data)
        
        assert updated_verification.used is True
        assert updated_verification.user_id == "user123"
        assert updated_verification.token == "token123"

    def test_delete_email_verification(self, db_session: Session):
        verification_data = EmailVerificationCreate(
            user_id="user123",
            token="token_to_delete",
            expires_at=datetime(2024, 12, 31, 23, 59, 59)
        )
        created_verification = crud_email_verifications.create(db_session, obj_in=verification_data)
        
        deleted_verification = crud_email_verifications.delete(db_session, id=created_verification.id)
        
        assert deleted_verification is not None
        assert deleted_verification.id == created_verification.id
        
        found_verification = crud_email_verifications.get(db_session, id=created_verification.id)
        assert found_verification is None

    def test_delete_email_verification_not_found(self, db_session: Session):
        result = crud_email_verifications.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_email_verifications(self, db_session: Session):
        verifications_data = [
            EmailVerificationCreate(user_id=f"user{i}", token=f"token{i}", expires_at=datetime(2024, 12, 31, 23, 59, 59))
            for i in range(5)
        ]
        
        for verification_data in verifications_data:
            crud_email_verifications.create(db_session, obj_in=verification_data)
        
        verifications = crud_email_verifications.get_multi(db_session, skip=0, limit=10)
        
        assert len(verifications) == 5
        assert all(isinstance(verification, EmailVerification) for verification in verifications)

    def test_get_multi_email_verifications_with_pagination(self, db_session: Session):
        verifications_data = [
            EmailVerificationCreate(user_id=f"user{i}", token=f"token{i}", expires_at=datetime(2024, 12, 31, 23, 59, 59))
            for i in range(10)
        ]
        
        for verification_data in verifications_data:
            crud_email_verifications.create(db_session, obj_in=verification_data)
        
        first_page = crud_email_verifications.get_multi(db_session, skip=0, limit=4)
        second_page = crud_email_verifications.get_multi(db_session, skip=4, limit=4)
        
        assert len(first_page) == 4
        assert len(second_page) == 4
        
        first_ids = {verification.id for verification in first_page}
        second_ids = {verification.id for verification in second_page}
        assert first_ids.isdisjoint(second_ids)