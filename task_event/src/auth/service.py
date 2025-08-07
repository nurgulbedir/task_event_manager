# src/auth/service.py - DOĞRU VE TAM HALİ

import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from . import security
from .models import UserCreate
from src.entities.user import User
from src.database.dependencies import get_db

# --- ÖNCEKİ FONKSİYONLAR (DEĞİŞİKLİK YOK) ---

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    # 1. ADIM (YENİ): E-postanın zaten var olup olmadığını kontrol et.
    #    Bunun için daha önce yazdığımız get_user_by_email fonksiyonunu kullanıyoruz.
    existing_user = get_user_by_email(db, email=user.email)

    # 2. ADIM (YENİ): Eğer kullanıcı bulunduysa, bir hata fırlat ve işlemi durdur.
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # 400: Hatanın istemciden kaynaklandığını belirtir.
            detail="Bu e-posta adresi zaten kayıtlı."
        )

    # 3. ADIM (ESKİ): Eğer e-posta yeni ise, normal kayıt işlemine devam et.
    hashed_password = security.get_password_hash(user.password)
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

def get_current_user(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# --- YENİ EKLENEN BAĞIMLILIK FONKSİYONU ---

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_dependency(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_current_user(token=token, db=db)

