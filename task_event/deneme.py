import psycopg2

try:

    conn = psycopg2.connect(
        host="localhost",           # Genellikle 'localhost' kalır
        database="task_event_db",  # Bağlanmak istediğiniz veritabanının adı
        user="postgres",      # PostgreSQL kullanıcı adınız
        password="123456"         # PostgreSQL şifreniz
    )

    # Bağlantı başarılı olursa bu mesajı yazdırır
    print("PostgreSQL veritabanı bağlantısı başarılı!")

    # Bağlantıyı kapat
    conn.close()

except psycopg2.OperationalError as e:
    # Bağlantı başarısız olursa hatayı yazdırır
    print(f"Bağlantı hatası: {e}")

