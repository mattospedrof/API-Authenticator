from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import (
    UserCreate, UserLogin, TokenResponse,
    RefreshTokenRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=dict, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, payload.name, payload.email, payload.password)
    return {"message": "User registered successfully", "user_id": user.id}


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    tokens = auth_service.authenticate_user(db, payload.email, payload.password)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_access_token(db, payload.refresh_token)


@router.post("/forgot-password", status_code=200)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    auth_service.forgot_password(db, payload.email)
    return {"message": "If the email exists, a reset link was sent."}


@router.post("/reset-password", status_code=200)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    auth_service.reset_password(db, payload.token, payload.new_password)
    return {"message": "Password reset successfully"}
