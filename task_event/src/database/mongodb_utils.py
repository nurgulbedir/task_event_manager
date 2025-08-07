# src/database/mongodb_utils.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# .env dosyasından MongoDB bağlantı URL'sini alıyoruz.
MONGO_DATABASE_URL = os.getenv("MONGO_DATABASE_URL")

class MongoManager:
    client: AsyncIOMotorClient = None
    db = None

mongo_manager = MongoManager()

async def connect_to_mongo():
    print("Connecting to MongoDB...")
    mongo_manager.client = AsyncIOMotorClient(MONGO_DATABASE_URL)
    # Veritabanı adını da .env'den alabiliriz veya burada belirtebiliriz.
    mongo_manager.db = mongo_manager.client.get_database("task_event_comments_db")
    print("Successfully connected to MongoDB.")

async def close_mongo_connection():
    print("Closing MongoDB connection...")
    mongo_manager.client.close()
    print("MongoDB connection closed.")

def get_mongo_db():
    # Bu fonksiyon, API'lerimizde veritabanı nesnesini almak için kullanılacak.
    return mongo_manager.db