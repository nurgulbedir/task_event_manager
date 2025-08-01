# src/main.py - GÜNCELLENMİŞ HALİ

from fastapi import FastAPI
from .database.core import engine, Base
from .entities import user, task
from .auth import controller as auth_controller


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Görev ve Etkinlik Yönetim Sistemi",
    description="Bu API, kullanıcıların görevlerini ve etkinliklerini yönetmelerini sağlar.",
    version="1.0.0"
)

app.include_router(auth_controller.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "API'ye hoş geldiniz!"}


# --- YENİ EKLENEN TEŞHİS BÖLÜMÜ ---
# Uygulama başladığında, FastAPI'nin bildiği tüm rotaları terminale yazdırır.
print("--- UYGULAMANIN BİLDİĞİ AKTİF ROTALAR ---")
for route in app.routes:
    # Sadece bizim eklediğimiz rotaları (GET, POST vb.) göstermek için bir kontrol
    if hasattr(route, "methods"):
        print(f"Path: {route.path}, Methods: {list(route.methods)}, Name: {route.name}")
print("------------------------------------------")

