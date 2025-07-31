# src/auth/service.py
import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# Kendi yazdığımız modülleri import ediyoruz
from . import security  # security.py dosyamız
from .models import UserCreate  # models.py dosyamızdan
from src.entities.user import User  # entities klasöründen User veritabanı modelimiz


# --- KULLANICI OLUŞTURMA ---
def create_user(db: Session, user: UserCreate):
    # 1. Kullanıcının gönderdiği şifreyi alıp hash'liyoruz.
    hashed_password = security.get_password_hash(user.password)

    # 2. Veritabanına kaydedilecek User nesnesini oluşturuyoruz.
    #    Dikkat: `password` yerine `hashed_password`'ü kullanıyoruz.
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )

    # 3. Veritabanı işlemleri
    db.add(db_user)  # Yeni kullanıcıyı session'a ekle
    db.commit()  # Değişiklikleri veritabanına işle (kaydet)
    db.refresh(db_user)  # Oluşturulan kullanıcının son halini (ID'si atanmış) al

    return db_user


# --- TOKEN OLUŞTURMA ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    # Token'ın son kullanma tarihini belirliyoruz
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Eğer süre verilmezse 15 dakika geçerli olsun
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    # .env dosyasından aldığımız bilgilerle token'ı imzalıyoruz
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt