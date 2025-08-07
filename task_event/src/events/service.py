# src/events/service.py - TAM VE NİHAİ HALİ

from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from fastapi import HTTPException, status

# --- Proje İçi Gerekli Modüller ---
from . import models as event_models
from . import utils as event_utils  # <-- DTO dönüşümü için yardımcı fonksiyonumuzu import ediyoruz
from src.entities.event import Event as EventEntity
from src.entities.event_participant import EventParticipant as ParticipantEntity, ResponseStatus
from src.entities.user import User as UserEntity
from src.exceptions import EventNotFoundException, UnauthorizedException
from src.logger import get_logger

# --- Logger'ı Başlatma ---
logger = get_logger(__name__)


# CREATE
def create_event(db: Session, event: event_models.EventCreate, creator: UserEntity) -> event_models.Event:
    """Yeni bir etkinlik oluşturur ve davetlileri ekler. Sonuç olarak Pydantic DTO'su döndürür."""
    logger.debug(f"Service: Creating event '{event.title}' in DB for creator ID {creator.id}.")

    event_data = event.model_dump(exclude={"invitee_emails"})
    db_event = EventEntity(**event_data, creator_id=creator.id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    creator_participant = ParticipantEntity(event_id=db_event.id, user_id=creator.id, status=ResponseStatus.ACCEPTED)
    db.add(creator_participant)

    if event.invitee_emails:
        for email in event.invitee_emails:
            user_to_invite = db.query(UserEntity).filter(UserEntity.email == email).first()
            if user_to_invite and user_to_invite.id != creator.id:
                participant = ParticipantEntity(event_id=db_event.id, user_id=user_to_invite.id,
                                                status=ResponseStatus.PENDING)
                db.add(participant)
            elif not user_to_invite:
                logger.warning(f"While creating event, invitee email '{email}' was not found in the system. Skipping.")

    db.commit()
    db.refresh(db_event)
    logger.debug(f"Service: Event '{event.title}' and its participants committed to DB.")

    return event_utils.convert_db_event_to_dto(db_event)


# READ ALL (WITH FILTERS)
def get_events_for_user(db: Session, user: UserEntity, creator_only: bool = False,
                        status: Optional[ResponseStatus] = None) -> List[event_models.Event]:
    """Bir kullanıcının dahil olduğu etkinlikleri, filtrelere göre listeler. Sonuç olarak DTO listesi döndürür."""
    query = db.query(EventEntity).join(ParticipantEntity).filter(ParticipantEntity.user_id == user.id)

    if creator_only:
        query = query.filter(EventEntity.creator_id == user.id)
    if status:
        query = query.filter(ParticipantEntity.status == status)

    events_from_db = query.options(joinedload(EventEntity.participants).joinedload(ParticipantEntity.user)).all()

    return [event_utils.convert_db_event_to_dto(db_event) for db_event in events_from_db]


# READ ONE
def get_event_details_by_id(db: Session, event_id: int, user: UserEntity) -> event_models.Event | None:
    """ID ile belirtilen bir etkinliğin detaylarını DTO olarak getirir."""
    event_from_db = db.query(EventEntity).join(ParticipantEntity).filter(
        EventEntity.id == event_id,
        ParticipantEntity.user_id == user.id
    ).options(joinedload(EventEntity.participants).joinedload(ParticipantEntity.user)).first()

    if not event_from_db:
        return None

    return event_utils.convert_db_event_to_dto(event_from_db)


# UPDATE
def update_event_by_id(db: Session, event_id: int, event_update: event_models.EventUpdate,
                       user: UserEntity) -> event_models.Event:
    """Bir etkinliği günceller ve güncellenmiş halini DTO olarak döndürür."""
    db_event = db.query(EventEntity).filter(EventEntity.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Etkinlik bulunamadı.")

    if db_event.creator_id != user.id:
        logger.error(f"AUTHORIZATION FAILED: User '{user.email}' tried to update event ID {event_id}.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bu etkinliği güncelleme yetkiniz yok.")

    update_data = event_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return event_utils.convert_db_event_to_dto(db_event)


# DELETE
# src/events/service.py - YENİ HALİ
def delete_event_by_id(db: Session, event_id: int, user: UserEntity):
    logger.debug(f"Service: Attempting to fetch event ID {event_id} for deletion.")
    db_event = db.query(EventEntity).filter(EventEntity.id == event_id).first()

    if not db_event:
        # Artık sadece anlamlı, iş mantığı hatası fırlatıyoruz.
        raise EventNotFoundException(event_id=event_id)

    if db_event.creator_id != user.id:
        # Yine HTTP kodu düşünmüyoruz. Sadece "Yetkin Yok" diyoruz.
        logger.error(f"AUTHORIZATION FAILED: User '{user.email}' tried to delete event ID {event_id}.")
        raise UnauthorizedException(detail="Bu etkinliği silme yetkiniz yok.")

    db.delete(db_event)
    db.commit()
    logger.info(f"Service: Event ID {event_id} successfully deleted from DB.")

# RESPOND TO INVITATION
def respond_to_invitation(db: Session, event_id: int, current_user: UserEntity,
                          response: event_models.EventInvitationUpdate) -> ParticipantEntity:
    """Kullanıcının davetine yanıtını işler. Bu fonksiyon DTO değil, controller'ın ihtiyacı olan Participant Entity'sini döndürür."""
    participant_record = db.query(ParticipantEntity).filter(
        ParticipantEntity.event_id == event_id,
        ParticipantEntity.user_id == current_user.id
    ).first()

    if not participant_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bu etkinliğe bir davetiniz bulunmamaktadır.")

    participant_record.status = response.status
    db.add(participant_record)
    db.commit()
    db.refresh(participant_record)

    return participant_record