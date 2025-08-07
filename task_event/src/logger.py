# src/logger.py

import logging
import sys

# 1. Log formatımızı belirliyoruz.
# [Zaman] - [Log Seviyesi] - [Modül Adı] - [Mesaj]
log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# 2. Temel yapılandırmayı yapıyoruz.
logging.basicConfig(
    level=logging.DEBUG,  # Geliştirme aşamasında en düşük seviyeyi seçelim ki her şeyi görelim.
    format=log_format,
    datefmt=date_format,
    # Logları hem dosyaya hem de konsola yazdırmak için handler'ları burada belirtmiyoruz.
    # Onları aşağıda manuel olarak ekleyeceğiz.
    stream=sys.stdout, # Varsayılan olarak logları konsola (standart çıktı) yaz.
)

# 3. İsteğe bağlı olarak, logları bir dosyaya da yazmak için bir FileHandler oluşturabiliriz.
#    Bu, özellikle production ortamı için çok önemlidir.
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.WARNING) # Dosyaya sadece WARNING ve üzeri seviyedeki hataları yaz.
file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

# 4. Ana (root) logger'ı alıp ona file_handler'ı ekleyebiliriz.
# logging.getLogger().addHandler(file_handler) # Şimdilik bu satırı yorumda bırakalım, önce konsolda görelim.


def get_logger(name: str) -> logging.Logger:
    """
    Belirtilen isimle bir logger nesnesi döndürür.
    Bu fonksiyonu, projenin diğer dosyalarından logger'ı almak için kullanacağız.
    """
    return logging.getLogger(name)