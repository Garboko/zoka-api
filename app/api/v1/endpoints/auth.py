from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from uuid import uuid4
import logging

from app.database.session import get_db
from app.schemas.users import UserCreate, UserResponse, UserUpdate
from app.crud import users as crud_users
from app.crud import email_verifications as crud_email_verifications
from app.core.security import create_access_token
from app.core.config import settings
from app.schemas.email_verifications import EmailVerificationCreate, EmailVerificationUpdate
from app.core.dependencies import get_current_active_user
from app.services.email import email_service
from app.middleware.rate_limit import limiter

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour") 
async def register(
    request: Request, 
    user_in: UserCreate, 
    db: Session = Depends(get_db)
):
    
    user = crud_users.get_by_email(db, email=user_in.email)
    if user:
        logger.warning(f"Registration attempt with existing email: {user_in.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        user = crud_users.create(db, obj_in=user_in)
        logger.info(f"User registered: {user.email} (ID: {user.id})")
    except Exception as e:
        logger.error(f"Error creating user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    verification_token = str(uuid4())
    verification = EmailVerificationCreate(
        user_id=user.id,
        token=verification_token,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24)
    )
    crud_email_verifications.create(db, obj_in=verification)
    
    try:
        await email_service.send_verification_email(
            email=user.email,
            user_name=user.full_name,
            token=verification_token
        )
        logger.info(f"Verification email sent to {user.email}")
    except Exception as e:
        logger.error(f"Error sending verification email to {user.email}: {e}", exc_info=True)
    
    return user

@router.post("/login")
@limiter.limit("10/minute")  
async def login(
    request: Request,  
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    
    user = crud_users.authenticate(db, email=form_data.username, password=form_data.password)
    
    if not user:
        logger.warning(f"Failed login attempt for email: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        logger.warning(f"Login attempt for inactive user: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, 
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user.email} (ID: {user.id})")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/verify-email/{token}")
@limiter.limit("10/hour") 
async def verify_email(
    request: Request,
    token: str, 
    db: Session = Depends(get_db)
):
    
    verification = crud_email_verifications.get_by_token(db, token=token)
    
    if not verification:
        logger.warning(f"Invalid verification token: {token}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid verification token"
        )
    
    if verification.used:
        logger.warning(f"Verification token already used: {token}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token already used"
        )
    
    if verification.expires_at < datetime.now(timezone.utc):
        logger.warning(f"Verification token expired: {token}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expired"
        )
    
    user = crud_users.get(db, id=verification.user_id)
    if not user:
        logger.error(f"User not found for verification token: {token}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_update = UserUpdate(email_verified=True, is_active=True)
    crud_users.update(db, db_obj=user, obj_in=user_update)
    
    verification_update = EmailVerificationUpdate(used=True)
    crud_email_verifications.update(db, db_obj=verification, obj_in=verification_update)
    
    logger.info(f"Email verified for user: {user.email}")
    
    return {"message": "Email verified successfully"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return current_user