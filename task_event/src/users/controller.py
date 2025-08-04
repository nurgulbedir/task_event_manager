# src/users/controller.py - DÜZELTİLMİŞ VE EN TEMİZ HALİ

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# Gerekli fonksiyonları ve modelleri, tam ve doğru yollarıyla import ediyoruz
from src.auth.service import get_current_user_dependency
from src.database.dependencies import get_db
from . import models as user_models
from . import service as users_service

# ÖNEMLİ: user_models.User'ı doğrudan import etmek yerine,
# 'user_models' takma adıyla kullanmak, bu tür hataları önler.
# from .models import User as UserResponseModel <-- Bu satırı kullanmıyoruz.

router = APIRouter()

@router.get("/me", response_model=user_models.User)
def read_users_me(
    # Depends'in içine direkt olarak fonksiyonu yazıyoruz.
    # FastAPI, bu fonksiyondan dönen değeri current_user'a atayacak.
    current_user: user_models.User = Depends(get_current_user_dependency)
):
    return current_user

@router.get("/", response_model=List[user_models.User])
def read_users(
    # Bu API'yi korumak için de aynı, standart yöntemi kullanıyoruz.
    current_user: user_models.User = Depends(get_current_user_dependency),
    # Diğer parametreler (skip, limit, db) FastAPI tarafından ayrıca ele alınır.
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # Fonksiyonun içindeki mantık aynı kalır.
    users = users_service.get_users(db, skip=skip, limit=limit)
    return users