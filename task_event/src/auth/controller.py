# src/auth/controller.py - NİHAİ GÜNCELLENMİŞ HAL

from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth import service as auth_service
from src.auth.models import UserCreate, Token
from src.database.dependencies import get_db
from src.logger import get_logger
from src.rate_limiter import limiter

logger = get_logger(__name__)
router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
def register_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"New user registration attempt for email: '{user.email}' from IP: {request.client.host}")
    db_user = auth_service.create_user(db=db, user=user)
    logger.info(f"User '{user.email}' registered successfully.")
    return {"message": f"User registered successfully."}

@router.post("/login", response_model=Token)
@limiter.limit("100/minute")
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login attempt for user: '{form_data.username}' from IP: {request.client.host}")
    user = auth_service.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        logger.warning(f"Failed login for user: '{form_data.username}'. Incorrect email or password.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    logger.info(f"User '{form_data.username}' successfully authenticated.")
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = auth_service.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    logger.debug(f"Access token created for user '{user.email}'.")
    return {"access_token": access_token, "token_type": "bearer"}