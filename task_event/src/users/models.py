# src/users/models.py - GÜNCELLENMİŞ HALİ

from pydantic import BaseModel, EmailStr

# Kullanıcı bilgilerini API'de göstermek için ana model
class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        from_attributes = True

# Kullanıcı kendi bilgilerini güncellerken gönderilecek veri
class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None

# Kullanıcı şifresini değiştirirken gönderilecek veri
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str