# src/users/controller.py - TAM VE NİHAİ HALİ

from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from sqlalchemy.orm import Session
from typing import List

# --- Proje İçi Gerekli Modüller ---
from src.auth.service import get_current_user_dependency
from src.database.dependencies import get_db
from . import models as user_models
from . import service as users_service
from src.entities.user import User as UserEntity
from src.logger import get_logger
from src.rate_limiter import limiter, get_token_user

# --- Logger'ı Başlatma ---
logger = get_logger(__name__)
router = APIRouter()

@router.get("/me", response_model=user_models.User)
@limiter.limit("100/hour", key_func=get_token_user)
def read_users_me(request: Request, current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' requested their own data.")
    return current_user

@router.put("/me", response_model=user_models.User)
@limiter.limit("100/hour", key_func=get_token_user)
def update_current_user(request: Request, user_update: user_models.UserUpdate, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' is attempting to update their profile.")
    return users_service.update_user_me(db=db, user=current_user, user_update=user_update)

@router.patch("/me/password")
@limiter.limit("100/hour", key_func=get_token_user)
def update_current_user_password(request: Request, password_update: user_models.PasswordUpdate, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' is attempting to change their password.")
    users_service.update_password_me(db=db, user=current_user, password_update=password_update)
    logger.info(f"User '{current_user.email}' successfully changed their password.")
    return {"message": "Şifre başarıyla güncellendi."}

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("100/hour", key_func=get_token_user)
def delete_current_user(request: Request, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    user_email_before_delete = current_user.email
    logger.info(f"User '{user_email_before_delete}' is deleting their own account.")
    users_service.delete_user_me(db=db, user=current_user)
    logger.info(f"Account for user '{user_email_before_delete}' has been successfully deleted.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", response_model=List[user_models.User])
@limiter.limit("100/hour", key_func=get_token_user)
def read_users(request: Request, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency), skip: int = 0, limit: int = 100):
    logger.info(f"User '{current_user.email}' requested the list of all users. Skip: {skip}, Limit: {limit}.")
    return users_service.get_users(db, skip=skip, limit=limit)