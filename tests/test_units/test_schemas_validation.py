import pytest
from pydantic import ValidationError
from app.schemas.users import UserCreate, UserUpdate
from app.schemas.forms import FormCreate

class TestUserSchemaValidation:
    
    def test_user_create_valid(self):
        user = UserCreate(
            email="valid@example.com",
            full_name="Valid User",
            password="securepass123"
        )
        assert user.email == "valid@example.com"
        assert user.full_name == "Valid User"
    
    def test_user_create_invalid_email(self):
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="not-an-email",
                full_name="Test",
                password="pass123"
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("email",) for e in errors)
    
    def test_user_create_missing_fields(self):
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com") 

class TestFormSchemaValidation:
    
    def test_form_create_valid(self):
        form = FormCreate(
            title="Test Form",
            description="Description",
            user_id="user123",
            public_access=False
        )
        assert form.title == "Test Form"
    
    def test_form_create_missing_user_id(self):
        with pytest.raises(ValidationError):
            FormCreate(
                title="Test Form"
            )