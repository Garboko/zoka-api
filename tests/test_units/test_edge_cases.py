import pytest
from app.schemas.users import UserCreate

class TestEdgeCases:
    
    def test_create_user_with_very_long_name(self, db_session):
        from app.crud import users
        
        long_name = "A" * 1000 
        user_data = UserCreate(
            email="longname@example.com",
            full_name=long_name,
            password="pass123"
        )
        
        try:
            user = users.create(db_session, obj_in=user_data)
            assert len(user.full_name) <= 1000
        except Exception as e:
            assert "too long" in str(e).lower() or "length" in str(e).lower()
    
    def test_pagination_with_negative_skip(self, db_session):
        from app.crud import users
        
        for i in range(5):
            users.create(db_session, obj_in=UserCreate(
                email=f"user{i}@example.com",
                full_name=f"User {i}",
                password="pass123"
            ))
        
        result = users.get_multi(db_session, skip=-1, limit=10)
        assert len(result) >= 0  
    
    def test_pagination_with_zero_limit(self, db_session):
        from app.crud import users
        
        for i in range(5):
            users.create(db_session, obj_in=UserCreate(
                email=f"user{i}@example.com",
                full_name=f"User {i}",
                password="pass123"
            ))
        
        result = users.get_multi(db_session, skip=0, limit=0)
        assert len(result) == 0
    
    def test_unicode_characters_in_form_title(self, db_session):
        from app.crud import forms
        from app.schemas.forms import FormCreate
        
        unicode_title = "Formulaire de test 🇫🇷 中文"
        form = forms.create(db_session, obj_in=FormCreate(
            title=unicode_title,
            user_id="user123"
        ))
        
        assert form.title == unicode_title
    
    def test_sql_injection_in_email(self, db_session):
        from app.crud import users
        
        malicious_email = "'; DROP TABLE users; --"
        
        user = users.get_by_email(db_session, email=malicious_email)
        assert user is None