# src/exception_handlers.py

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .exceptions import DetailedHTTPException
from .logger import get_logger

logger = get_logger(__name__)


# 1. Kendi özel hata sınıfımız için bir handler
async def detailed_http_exception_handler(request: Request, exc: DetailedHTTPException):
    logger.error(
        f"DetailedHTTPException caught: Status={exc.status_code}, Detail={exc.detail}, Extra={exc.extra_info}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "extra_info": exc.extra_info},
    )


# 2. FastAPI'nin veri doğrulama hataları için bir handler (Örn: email formatı yanlış)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # exc.errors() -> Hangi alanda, ne tür bir hata olduğunu detaylı bir liste olarak verir.
    error_details = []
    for error in exc.errors():
        field = " -> ".join(map(str, error.get("loc", [])))
        message = error.get("msg")
        error_details.append(f"Alan '{field}': {message}")

    logger.warning(f"Request validation failed: {error_details}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "İstek verisi doğrulanamadı.", "errors": error_details},
    )


# 3. Yakalanmayan diğer tüm Python hataları için genel bir handler
async def generic_exception_handler(request: Request, exc: Exception):
    # Bu, kodumuzda beklemediğimiz bir hata (örn: NoneType error) olduğunda çalışır.
    # Bu tür hatalar kritik olduğu için ERROR seviyesinde loglanmalıdır.
    logger.error(f"An unhandled exception occurred: {exc}", exc_info=True)  # exc_info=True traceback'i loglar
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Sunucuda beklenmedik bir hata oluştu."},
    )