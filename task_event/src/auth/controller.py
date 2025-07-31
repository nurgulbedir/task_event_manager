# src/auth/controller.py
from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import service as auth_service
from .models import UserCreate, Token
from src.database.dependencies import get_db  # Veritabanı session'ı için bir yardımcı

# APIRouter, bu bölümdeki API'ları gruplamamızı sağlar.
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


# YENİ KULLANICI KAYDI İÇİN API
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Aynı e-posta ile başka bir kullanıcı var mı kontrolü (sonra eklenebilir)
    # ...

    # Servis katmanındaki fonksiyonumuzu çağırıyoruz
    db_user = auth_service.create_user(db=db, user=user)
    return {"message": f"User {db_user.email} registered successfully."}


# KULLANICI GİRİŞİ VE TOKEN ALMA İÇİN API
@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm, gelen istekte "username" ve "password" alanlarını arar.
    # Biz "username" olarak e-postayı kullanacağız.

    # Önce kullanıcının gerçekten var olup olmadığını ve şifrenin doğru olup olmadığını kontrol etmeliyiz.
    # Bunun için service katmanında yeni bir fonksiyona ihtiyacımız olacak.
    # Şimdilik bu kısmı geçici olarak yazalım ve sonra düzeltelim.
    # Bu kısım henüz çalışmayacak!

    # TODO: auth_service içinde authenticate_user fonksiyonu yazılacak.
    user = None  # Geçici
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}