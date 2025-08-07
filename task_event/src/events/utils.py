# src/events/utils.py

# Gerekli importlar
from . import models as event_models
from src.entities.event import Event as EventEntity


# Fonksiyon tanımı
def convert_db_event_to_dto(db_event: EventEntity) -> event_models.Event:
    """
    Bir SQLAlchemy Event nesnesini (veritabanı nesnesi),
    bir Pydantic Event DTO'suna (API yanıt modeli) dönüştürür.
    """
    # 1. Katılımcı listesini DTO'ya çevir.
    participants_dto = [
        event_models.EventParticipantResponse(
            user_id=p.user.id,
            user_email=p.user.email,
            status=p.status
        ) for p in db_event.participants
    ]

    # 2. Ana Event DTO'sunu oluştur.
    event_dto = event_models.Event(
        id=db_event.id,
        title=db_event.title,
        description=db_event.description,
        start_time=db_event.start_time,
        end_time=db_event.end_time,
        creation_date=db_event.creation_date,
        creator_id=db_event.creator_id,
        participants=participants_dto
    )

    return event_dto