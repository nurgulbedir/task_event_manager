# exceptions.py

class DetailedHTTPException(Exception):
    """
    HTTPException'a benzeyen ama daha fazla detay taşıyabilen
    bizim temel özel hata sınıfımız. Uygulamamızdaki tüm anlamsal
    hatalar bu sınıftan türeyecek.
    """
    def __init__(self, status_code: int, detail: str = None, **kwargs):
        self.status_code = status_code
        self.detail = detail
        # Hata hakkında loglama veya istemci için ekstra bilgi (örn: hangi ID bulunamadı)
        # taşımak için bir sözlük (dictionary).
        self.extra_info = kwargs
        super().__init__(self.detail)

# --- Genel Amaçlı Hata Sınıfları ---

class NotFoundException(DetailedHTTPException):
    """
    Bir kaynak (kullanıcı, görev, etkinlik vb.) bulunamadığında
    kullanılacak genel "Bulunamadı" hatası.
    """
    def __init__(self, detail: str = "İstenen kaynak bulunamadı.", **kwargs):
        # Bu hata her zaman 404 durum koduyla eşleşir.
        super().__init__(status_code=404, detail=detail, **kwargs)

class UnauthorizedException(DetailedHTTPException):
    """
    Bir kullanıcının, bir işlemi yapmaya yetkisi olmadığında
    kullanılacak genel "Yetkisiz" hatası.
    """
    def __init__(self, detail: str = "Bu işlemi gerçekleştirme yetkiniz bulunmamaktadır.", **kwargs):
        # Bu hata her zaman 403 durum koduyla eşleşir.
        super().__init__(status_code=403, detail=detail, **kwargs)

class BadRequestException(DetailedHTTPException):
    """
    İstemciden gelen verinin anlamsal olarak hatalı olduğu durumlar için
    (örn: şifrelerin eşleşmemesi) kullanılacak genel "Hatalı İstek" hatası.
    """
    def __init__(self, detail: str = "İstek geçersiz veya hatalı.", **kwargs):
        # Bu hata her zaman 400 durum koduyla eşleşir.
        super().__init__(status_code=400, detail=detail, **kwargs)


# --- Spesifik Hata Sınıfları (Daha Anlamlı Hatalar için) ---

class UserNotFoundException(NotFoundException):
    """
    Özellikle bir kullanıcı bulunamadığında daha detaylı bir mesaj
    vermek için kullanılır. NotFoundException'dan miras alır.
    """
    def __init__(self, user_identifier: str | int):
        super().__init__(
            detail=f"Kullanıcı bulunamadı: {user_identifier}",
            # Hata yakalayıcının veya logların kullanması için ekstra bilgi
            user_identifier=user_identifier
        )

class EventNotFoundException(NotFoundException):
    """
    Özellikle bir etkinlik bulunamadığında kullanılır.
    """
    def __init__(self, event_id: int):
        super().__init__(
            detail=f"Etkinlik ID: {event_id} bulunamadı.",
            event_id=event_id
        )