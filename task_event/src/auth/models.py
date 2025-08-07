# src/auth/models.py
from pydantic import BaseModel, EmailStr

# Kullanıcı oluştururken (kayıt olurken) API'ye gönderilecek veri modeli
class UserCreate(BaseModel):
    email: EmailStr  # Pydantic, bunun geçerli bir e-posta formatı olduğunu kontrol eder.
    password: str
    first_name: str
    last_name: str

# Kullanıcıya token döndürürken kullanılacak model
class Token(BaseModel):
    access_token: str
    token_type: str

# Token'ın içine gömeceğimiz verinin modeli (payload)
class TokenData(BaseModel):
    email: str | None = None