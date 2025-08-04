# src/users/models.py
from pydantic import BaseModel, EmailStr

# Kullanıcı bilgilerini API'de göstermek için kullanılacak model.
# Dikkat: Şifre alanı burada YOKTUR.
class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        from_attributes = True # SQLAlchemy nesnesini Pydantic modeline dönüştürür.