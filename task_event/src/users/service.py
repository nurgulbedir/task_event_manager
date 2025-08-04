# src/users/service.py - OLMASI GEREKEN DOĞRU İÇERİK

from sqlalchemy.orm import Session
from src.entities.user import User

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Veritabanından kullanıcı listesini çeker.
    """
    return db.query(User).offset(skip).limit(limit).all()