# src/main.py - GÜNCELLENMİŞ HALİ

from fastapi import FastAPI
from .database.core import engine, Base
from .entities import user, task



# Yeni controller'ımızı import ediyoruz
from .auth import controller as auth_controller

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Görev ve Etkinlik Yönetim Sistemi",
    description="Bu API, kullanıcıların görevlerini ve etkinliklerini yönetmelerini sağlar.",
    version="1.0.0"
)

# Auth Router'ını ana uygulamaya dahil ediyoruz.
# prefix="/auth" -> tüm bu router'daki URL'ler /auth ile başlayacak (örn: /auth/register)
# tags=["Authentication"] -> FastAPI'nin otomatik dokümantasyonunda gruplama yapacak.
app.include_router(auth_controller.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "API'ye hoş geldiniz!"}