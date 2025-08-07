# src/users/service.py - TAM VE NİHAİ HALİ

from sqlalchemy.orm import Session
from typing import List

# --- Proje İçi Gerekli Modüller ---
from src.entities.user import User as UserEntity
from . import models as user_models
from . import utils as user_utils
from src.auth import security
from src.exceptions import BadRequestException
from src.logger import get_logger

# --- Logger'ı Başlatma ---
logger = get_logger(__name__)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[user_models.User]:
    """Tüm kullanıcıları DTO listesi olarak döndürür."""
    users_from_db = db.query(UserEntity).offset(skip).limit(limit).all()
    return [user_utils.convert_db_user_to_dto(db_user) for db_user in users_from_db]


def update_user_me(db: Session, user: UserEntity, user_update: user_models.UserUpdate) -> user_models.User:
    """Mevcut kullanıcıyı günceller ve güncellenmiş halini DTO olarak döndürür."""
    update_data = user_update.model_dump(exclude_unset=True)
    logger.debug(f"Updating user '{user.email}' with data: {update_data}")
    for key, value in update_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_utils.convert_db_user_to_dto(user)


def update_password_me(db: Session, user: UserEntity, password_update: user_models.PasswordUpdate) -> UserEntity:
    """
    Mevcut kullanıcının parolasını günceller. Başarısız olursa Exception fırlatır.
    """
    if not security.verify_password(password_update.current_password, user.hashed_password):
        logger.debug(f"Password verification failed for user '{user.email}'.")
        raise BadRequestException(detail="Mevcut şifre yanlış.")

    if password_update.current_password == password_update.new_password:
        logger.warning(f"User '{user.email}' tried to set new password same as the current one.")
        raise BadRequestException(detail="Yeni şifre, mevcut şifrenizle aynı olamaz.")

    hashed_password = security.get_password_hash(password_update.new_password)
    logger.debug(f"New password has been hashed for user '{user.email}'.")
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()

    return user


def delete_user_me(db: Session, user: UserEntity):
    """Mevcut kullanıcıyı siler."""
    db.delete(user)
    db.commit()