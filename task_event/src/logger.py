# src/logger.py

import logging
import sys


def setup_logging():
    """
    Tüm loglama altyapısını kuran merkezi fonksiyon.
    Bu fonksiyon main.py'dan uygulama başlarken çağrılacak.
    """
    # 1. Log formatlarımızı tanımlıyoruz.
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    # 2. Ana (root) logger'ı alıyoruz.
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Ana filtre her şeyi yakalasın.

    # Önceki tüm handler'ları temizleyerek sıfırdan başlıyoruz.
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 3. Konsol için Handler (Seviye: INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Konsolda sadece INFO ve üzerini göster.
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 4. Dosya için Handler (Seviye: WARNING)
    file_handler = logging.FileHandler("app.log", mode='a')
    file_handler.setLevel(logging.WARNING)  # Dosyaya sadece WARNING ve üzerini yaz.
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # 5. "Gürültücü" kütüphaneleri susturuyoruz.
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("passlib").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)  # Uvicorn'un trafik loglarını da susturalım.

    # Bu mesaj, yapılandırmanın çalıştığını bize gösterecek.
    logging.getLogger(__name__).info("Loglama sistemi başarıyla kuruldu.")


def get_logger(name: str) -> logging.Logger:
    """Belirtilen isimle bir logger nesnesi döndürür."""
    return logging.getLogger(name)