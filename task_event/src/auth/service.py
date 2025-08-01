# src/auth/service.py
import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# Kendi yazdığımız modülleri import ediyoruz
from . import security  # security.py dosyamız
from .models import UserCreate  # models.py dosyamızdan
from src.entities.user import User  # entities klasöründen User veritabanı modelimiz

# src/auth/service.py - ORİJİNAL VE TEMİZ HALİ


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
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


# src/auth/service.py - authenticate_user FONKSİYONUNUN GEÇİCİ DEBUG HALİ

def authenticate_user(db: Session, email: str, password: str):
    print("\n--- authenticate_user fonksiyonu çağrıldı ---")
    print(f"Aranan Email: '{email}'")

    user = get_user_by_email(db, email=email)

    if not user:
        print(">>> HATA NOKTASI 1: get_user_by_email fonksiyonu kullanıcıyı BULAMADI.")
        print("------------------------------------------\n")
        return False

    print(f"Kullanıcı bulundu: {user.email}")

    if not security.verify_password(password, user.hashed_password):
        print(">>> HATA NOKTASI 2: security.verify_password fonksiyonu BAŞARISIZ OLDU (Şifre eşleşmedi).")
        print("------------------------------------------\n")
        return False

    print(">>> BAŞARILI: Kullanıcı bulundu ve şifre doğrulandı.")
    print("------------------------------------------\n")
    return user



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt