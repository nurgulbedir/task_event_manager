# src/comments/service.py - TAM VE NİHAİ HALİ

from datetime import datetime
from typing import List
from . import models as comment_models
from src.database.mongodb_utils import get_mongo_db
from src.entities.user import User as UserEntity


# --- YORUM OLUŞTURMA ---
async def create_comment(event_id: int, comment_data: comment_models.CommentCreate, author: UserEntity):
    """
    Yeni bir yorumu MongoDB'ye kaydeder.
    Gelen verideki tüm alanları dinamik olarak kaydeder.
    """
    db = get_mongo_db()

    comment_payload = comment_data.model_dump(exclude_unset=True)

    comment_document = {
        **comment_payload,
        "event_id": event_id,
        "author_id": author.id,
        "author_email": author.email,
        "created_at": datetime.utcnow()
    }

    result = await db.comments.insert_one(comment_document)
    created_comment = await db.comments.find_one({"_id": result.inserted_id})
    return created_comment


# --- YORUMLARI LİSTELEME (YENİ EKLENEN FONKSİYON) ---
async def get_comments_for_event(event_id: int) -> List[dict]:
    """
    Belirli bir event_id'ye ait tüm yorumları MongoDB'den çeker.
    """
    db = get_mongo_db()

    comments = []
    # db.comments.find({"event_id": event_id}) -> Bu, bir "cursor" (imleç) döndürür.
    # Bu cursor üzerinde asenkron olarak döngü kurarak tüm dökümanları alıyoruz.
    async for comment in db.comments.find({"event_id": event_id}):
        comments.append(comment)

    return comments