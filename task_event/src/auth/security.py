# src/auth/security.py
from passlib.context import CryptContext

# Şifreleme için hangi algoritmayı kullanacağımızı belirtiyoruz.
# "bcrypt" şu anki en popüler ve güvenli seçeneklerden biridir.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Girilen şifre ile veritabanındaki hash'lenmiş şifreyi karşılaştırır."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Verilen şifreyi hash'ler."""
    return pwd_context.hash(password)