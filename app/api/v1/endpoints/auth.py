from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from uuid import uuid4

from app.database.session import get_db
from app.schemas.users import UserCreate, UserResponse, UserLogin, UserUpdate
from app.crud import users as crud_users
from app.crud import email_verifications as crud_email_verifications
from app.core.security import create_access_token
from app.core.config import settings
from app.schemas.email_verifications import EmailVerificationCreate, EmailVerificationUpdate
from app.core.dependencies import get_current_active_user  
from app.services.email import email_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = crud_users.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = crud_users.create(db, obj_in=user_in)
    
    verification_token = str(uuid4())
    verification = EmailVerificationCreate(
        user_id=user.id,
        token=verification_token,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    crud_email_verifications.create(db, obj_in=verification)
    
    try:
        await email_service.send_verification_email(
            email=user.email,
            user_name=user.full_name,
            token=verification_token
        )
    except Exception as e:
        print(f"Error sending verification email: {e}")
    
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_users.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/verify-email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    verification = crud_email_verifications.get_by_token(db, token=token)
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid verification token"
        )
    
    if verification.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token already used"
        )
    
    if verification.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expired"
        )
    
    user = crud_users.get(db, id=verification.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_update = UserUpdate(email_verified=True, is_active=True)
    crud_users.update(db, db_obj=user, obj_in=user_update)
    
    verification_update = EmailVerificationUpdate(used=True)
    crud_email_verifications.update(db, db_obj=verification, obj_in=verification_update)
    
    return {"message": "Email verified successfully"}

@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return current_user