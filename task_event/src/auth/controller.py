# src/auth/controller.py
from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import service as auth_service
from .models import UserCreate, Token
from src.database.dependencies import get_db  # Veritabanı session'ı için bir yardımcı


# DİKKAT: Router'ı artık prefix OLMADAN oluşturuyoruz.
# Çünkü bu yönetim sadece main.py'de yapılmalı.
router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = auth_service.create_user(db=db, user=user)
    print("calıştı")
    return {"message": f"User {db_user.email} registered successfully."}


# src/auth/controller.py - YENİ DEBUG KODU

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("\n--- /login endpoint'i tetiklendi ---")

    # Adım 1: Gelen form verisini kontrol et
    print(f"Gelen form verisi (username): '{form_data.username}'")
    print(f"Gelen form verisi (password): '{form_data.password}'")

    # Adım 2: authenticate_user fonksiyonunu çağırmadan hemen önce
    print(">>> auth_service.authenticate_user çağrılmak üzere...")

    user = auth_service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )

    # Adım 3: authenticate_user fonksiyonundan dönen sonucu kontrol et
    if not user:
        print(">>> authenticate_user 'False' veya 'None' döndürdü. Hata veriliyor.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Adım 4: Başarılı doğrulama
    print(f">>> authenticate_user başarılı, kullanıcı: {user.email}")
    print("Token oluşturuluyor...")

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}