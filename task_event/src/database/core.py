# src/database/core.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv() # bunlar fonksiyon mu anlayamadım (getenv dotenv).env dosyasındaki değişkenleri yükler

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy motorunu oluşturur
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Veritabanı oturumları için bir fabrika
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modellerimizin miras alacağı temel sınıf
Base = declarative_base()