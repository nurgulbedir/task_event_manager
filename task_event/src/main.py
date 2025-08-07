# src/main.py

import sys
import os

# --- Adım 1: Proje Kök Dizinini Python Path'ine Ekleme ---
# Bu, import hatalarını en başından önler.
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)
sys.path.append(project_root)

# --- Adım 2: Loglama Sistemini, Diğer Her Şeyden Önce Kurma ---
# Bu, diğer kütüphanelerin bizim ayarlarımızı ezmesini engeller.
from src.logger import setup_logging
setup_logging()

# --- Adım 3: Diğer Tüm Gerekli Modülleri Import Etme ---
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

# Veritabanı ve Modül Controller'ları
from src.database.core import engine, Base
from src.database.mongodb_utils import connect_to_mongo, close_mongo_connection
from src.entities import user, task, event, event_participant
from src.auth import controller as auth_controller
from src.users import controller as users_controller
from src.tasks import controller as tasks_controller
from src.events import controller as events_controller
from src.comments import controller as comments_controller
from src.files import controller as files_controller

# Merkezi Hata Yönetimi
from src.exceptions import DetailedHTTPException
from src.exception_handlers import (
    detailed_http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

# Rate Limiting Sistemi
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from src.rate_limiter import limiter

# --- Adım 4: Veritabanı Tablolarını Oluşturma (PostgreSQL) ---
Base.metadata.create_all(bind=engine)

# --- Adım 5: FastAPI Uygulamasını Oluşturma ---
app = FastAPI(
    title="Görev ve Etkinlik Yönetim Sistemi",
    description="Bu API, kullanıcıların görevlerini ve etkinliklerini yönetmelerini sağlar.",
    version="1.0.0"
)

# --- Adım 6: Uygulama Başlangıç ve Kapanış Olayları (MongoDB Bağlantısı) ---
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# --- Adım 7: Middleware ve Handler'ları Ekleme ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(DetailedHTTPException, detailed_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# --- Adım 8: Static Dosya Sunumunu Aktif Etme ---
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Adım 9: Router'ları Uygulamaya Dahil Etme ---
app.include_router(auth_controller.router, prefix="/auth", tags=["Authentication"])
app.include_router(users_controller.router, prefix="/users", tags=["Users"])
app.include_router(tasks_controller.router, prefix="/tasks", tags=["Tasks"])
app.include_router(events_controller.router, prefix="/events", tags=["Events"])
app.include_router(comments_controller.router, prefix="/events/{event_id}/comments", tags=["Comments"])
app.include_router(files_controller.router, prefix="/files", tags=["Files"])


# --- Adım 10: Kök (Root) Endpoint ---
@app.get("/")
def read_root(request: Request):
    return {"message": "API'ye hoş geldiniz!"}
