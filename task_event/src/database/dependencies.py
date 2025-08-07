# src/database/dependencies.py

from .core import SessionLocal

# Bu fonksiyon, her API isteği için yeni bir veritabanı oturumu (session)
# oluşturacak, isteğin sonunda oturumu kapatacak ve bu sayede kaynakları
# serbest bırakacak. FastAPI'nin "Dependency Injection" sistemini kullanır.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()