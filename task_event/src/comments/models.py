# src/comments/models.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Any
from bson import ObjectId
from pydantic_core import core_schema


# --- PyObjectId Sınıfı (Pydantic v2 Uyumlu) ---
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: Any,
    ) -> core_schema.CoreSchema:
        def validate(v: Any) -> ObjectId:
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid objectid")
            return ObjectId(v)

        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(validate)
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )


# --- Yorum Modelleri ---

# Yorum oluşturulurken API'ye gönderilecek esnek veri modeli
class CommentCreate(BaseModel):
    comment_text: str
    emoji: Optional[str] = None
    attachments: Optional[List[str]] = None


# MongoDB'den API'ye yanıt olarak döndürülecek tam yorum modeli
class CommentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    event_id: int
    comment_text: str
    emoji: Optional[str] = None
    attachments: Optional[List[str]] = None
    author_id: int
    author_email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



from datetime import datetime
from . import models as comment_models
from src.database.mongodb_utils import get_mongo_db
from src.entities.user import User as UserEntity


async def create_comment(event_id: int, comment_data: comment_models.CommentCreate, author: UserEntity):
    """
    Yeni bir yorumu MongoDB'ye kaydeder.
    Gelen verideki tüm alanları dinamik olarak kaydeder.
    """
    db = get_mongo_db()

    # Pydantic modelini bir dictionary'ye çeviriyoruz.
    # exclude_unset=True sayesinde sadece gönderilen opsiyonel alanlar (emoji vb.) dahil edilir.
    comment_payload = comment_data.model_dump(exclude_unset=True)

    # Sunucu tarafında eklediğimiz zorunlu bilgileri de ekliyoruz.
    comment_document = {
        **comment_payload,
        "event_id": event_id,
        "author_id": author.id,
        "author_email": author.email,
        "created_at": datetime.utcnow()
    }

    # Dökümanı "comments" koleksiyonuna ekliyoruz.
    result = await db.comments.insert_one(comment_document)

    # Eklenen dökümanı ID'si ile veritabanından geri çekip döndürüyoruz.
    created_comment = await db.comments.find_one({"_id": result.inserted_id})

    return created_comment