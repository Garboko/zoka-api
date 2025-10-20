import pytest
from fastapi.testclient import TestClient

class TestAuthEndpoints:
    
    def test_register_success(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "full_name": "New User",
                "password": "securepass123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert "id" in data
        assert data["is_active"] == False  
        assert data["email_verified"] == False
    
    def test_register_duplicate_email(self, client):
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "full_name": "User 1",
                "password": "pass123"
            }
        )
        
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "full_name": "User 2",
                "password": "pass456"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_invalid_email(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "full_name": "Test User",
                "password": "pass123"
            }
        )
        assert response.status_code == 422  
    
    def test_login_success(self, client, db_session):
        from app.crud import users as crud_users
        from app.schemas.users import UserCreate
        
        user_data = UserCreate(
            email="login@example.com",
            full_name="Login User",
            password="correctpass"
        )
        user = crud_users.create(db_session, obj_in=user_data)
        
        from app.schemas.users import UserUpdate
        crud_users.update(
            db_session, 
            db_obj=user, 
            obj_in=UserUpdate(is_active=True)
        )
        
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "login@example.com",  
                "password": "correctpass"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, db_session):
        from app.crud import users as crud_users
        from app.schemas.users import UserCreate, UserUpdate
        
        user_data = UserCreate(
            email="test@example.com",
            full_name="Test",
            password="correctpass"
        )
        user = crud_users.create(db_session, obj_in=user_data)
        crud_users.update(
            db_session, 
            db_obj=user, 
            obj_in=UserUpdate(is_active=True)
        )
        
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401
    
    def test_login_inactive_user(self, client, db_session):
        from app.crud import users as crud_users
        from app.schemas.users import UserCreate
        
        user_data = UserCreate(
            email="inactive@example.com",
            full_name="Inactive",
            password="pass123"
        )
        crud_users.create(db_session, obj_in=user_data)
        
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "inactive@example.com",
                "password": "pass123"
            }
        )
        assert response.status_code == 400
        assert "inactive" in response.json()["detail"].lower()
    
    def test_get_current_user(self, client, db_session):
        from app.crud import users as crud_users
        from app.schemas.users import UserCreate, UserUpdate
        from app.core.security import create_access_token
        
        user_data = UserCreate(
            email="current@example.com",
            full_name="Current User",
            password="pass123"
        )
        user = crud_users.create(db_session, obj_in=user_data)
        crud_users.update(
            db_session,
            db_obj=user,
            obj_in=UserUpdate(is_active=True)
        )
        
        token = create_access_token(data={"sub": user.id})
        
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "current@example.com"
        assert data["id"] == user.id
    
    def test_get_current_user_invalid_token(self, client):
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401