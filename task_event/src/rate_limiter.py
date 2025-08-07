# rate_limiter.py

from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request, Depends
from sqlalchemy.orm import Session

# Kendi modüllerimizden importlar. Bu yolların doğru olduğundan emin ol.
# Eğer src klasörün yoksa, başındaki "src." kısmını sil.
from src.auth.service import get_current_user
from src.database.dependencies import get_db

# 1. IP bazlı anahtar fonksiyonu (en basit)
# Bu fonksiyon, isteği yapanın IP adresini döndürür.
def get_ipaddr(request: Request) -> str:
    return get_remote_address(request)

# 2. Token bazlı anahtar fonksiyonu (daha karmaşık)
# Bu fonksiyon, isteğin token'ını çözümleyip içindeki kullanıcıyı döndürür.
def get_token_user(request: Request, db: Session = Depends(get_db)) -> str:
    auth_header = request.headers.get("authorization")
    if not auth_header:
        return get_ipaddr(request) # Token yoksa, IP'ye göre limitle

    try:
        token_type, token = auth_header.split()
        if token_type.lower() != "bearer":
            return get_ipaddr(request)
    except (ValueError, AttributeError):
        return get_ipaddr(request)

    try:
        user = get_current_user(token=token, db=db)
        return user.email # Kullanıcının e-postası, onun benzersiz anahtarıdır.
    except Exception:
        # Token geçersizse veya bir hata olursa, yine IP'ye göre limitle
        return get_ipaddr(request)


# 3. Limiter nesnemizi oluşturuyoruz.
# Varsayılan anahtar fonksiyon olarak IP adresini kullanıyoruz.
limiter = Limiter(key_func=get_remote_address)