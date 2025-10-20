import pytest
from fastapi.testclient import TestClient

class TestFormPermissions:
    
    def test_user_can_access_own_form(self, client, db_session):
        from app.crud import users, forms
        from app.schemas.users import UserCreate, UserUpdate
        from app.schemas.forms import FormCreate
        from app.core.security import create_access_token
        
        user = users.create(db_session, obj_in=UserCreate(
            email="owner@example.com",
            full_name="Owner",
            password="pass123"
        ))
        users.update(db_session, db_obj=user, obj_in=UserUpdate(is_active=True))
        
        form = forms.create(db_session, obj_in=FormCreate(
            title="My Form",
            user_id=user.id
        ))
        
        token = create_access_token(data={"sub": user.id})
        
        response = client.get(
            f"/api/v1/forms/{form.id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
    
    def test_user_cannot_access_other_form(self, client, db_session):
        from app.crud import users, forms
        from app.schemas.users import UserCreate, UserUpdate
        from app.schemas.forms import FormCreate
        from app.core.security import create_access_token
        
        owner = users.create(db_session, obj_in=UserCreate(
            email="owner@example.com",
            full_name="Owner",
            password="pass123"
        ))
        other = users.create(db_session, obj_in=UserCreate(
            email="other@example.com",
            full_name="Other",
            password="pass456"
        ))
        users.update(db_session, db_obj=owner, obj_in=UserUpdate(is_active=True))
        users.update(db_session, db_obj=other, obj_in=UserUpdate(is_active=True))
        
        form = forms.create(db_session, obj_in=FormCreate(
            title="Owner's Form",
            user_id=owner.id
        ))
        
        token = create_access_token(data={"sub": other.id})
        
        response = client.get(
            f"/api/v1/forms/{form.id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
    
    def test_unauthenticated_cannot_access_form(self, client, db_session):
        from app.crud import users, forms
        from app.schemas.users import UserCreate
        from app.schemas.forms import FormCreate
        
        user = users.create(db_session, obj_in=UserCreate(
            email="user@example.com",
            full_name="User",
            password="pass123"
        ))
        form = forms.create(db_session, obj_in=FormCreate(
            title="Form",
            user_id=user.id
        ))
        
        response = client.get(f"/api/v1/forms/{form.id}")
        assert response.status_code == 401