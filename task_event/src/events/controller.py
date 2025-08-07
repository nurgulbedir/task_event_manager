# src/events/controller.py - TAM VE NİHAİ HALİ

from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from sqlalchemy.orm import Session
from typing import List, Optional

# --- Proje İçi Gerekli Modüller ---
from . import models as event_models
from . import service as event_service
from . import utils as event_utils
from src.database.dependencies import get_db
from src.auth.service import get_current_user_dependency
from src.entities.user import User as UserEntity
from src.entities.event_participant import ResponseStatus
from src.logger import get_logger
from src.rate_limiter import limiter, get_token_user

# --- Logger'ı Başlatma ---
logger = get_logger(__name__)
router = APIRouter()

@router.post("/", response_model=event_models.Event, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/hour", key_func=get_token_user)
def create_event(request: Request, event: event_models.EventCreate, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' is creating event: '{event.title}'.")
    db_event = event_service.create_event(db=db, event=event, creator=current_user)
    logger.info(f"Event ID {db_event.id} created by '{current_user.email}'.")
    return event_utils.convert_db_event_to_dto(db_event)

@router.get("/", response_model=List[event_models.Event])
@limiter.limit("100/hour", key_func=get_token_user)
def get_all_events_for_current_user(request: Request, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency), creator_only: bool = False, status: Optional[ResponseStatus] = None):
    logger.info(f"User '{current_user.email}' requested events. Filters - creator_only:{creator_only}, status:{status}")
    db_events = event_service.get_events_for_user(db=db, user=current_user, creator_only=creator_only, status=status)
    logger.debug(f"Found {len(db_events)} events for user '{current_user.email}'.")
    return [event_utils.convert_db_event_to_dto(db_event) for db_event in db_events]

@router.get("/{event_id}", response_model=event_models.Event)
@limiter.limit("100/hour", key_func=get_token_user)
def get_single_event_details(request: Request, event_id: int, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' requested details for event ID: {event_id}.")
    db_event = event_service.get_event_details_by_id(db=db, event_id=event_id, user=current_user)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı veya görme yetkiniz yok.")
    return event_utils.convert_db_event_to_dto(db_event)

@router.put("/{event_id}", response_model=event_models.Event)
@limiter.limit("100/hour", key_func=get_token_user)
def update_an_event(request: Request, event_id: int, event_update: event_models.EventUpdate, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' is updating event ID: {event_id}.")
    updated_event = event_service.update_event_by_id(db=db, event_id=event_id, event_update=event_update, user=current_user)
    logger.info(f"Event ID {event_id} updated by '{current_user.email}'.")
    return event_utils.convert_db_event_to_dto(updated_event)

@router.patch("/{event_id}/invitation", response_model=event_models.EventParticipantResponse)
@limiter.limit("100/hour", key_func=get_token_user)
def respond_to_event_invitation(request: Request, event_id: int, invitation_update: event_models.EventInvitationUpdate, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' responding to invite for event {event_id} with status '{invitation_update.status.value}'.")
    updated_participant = event_service.respond_to_invitation(db=db, event_id=event_id, current_user=current_user, response=invitation_update)
    return event_models.EventParticipantResponse(user_id=updated_participant.user.id, user_email=updated_participant.user.email, status=updated_participant.status)

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("100/hour", key_func=get_token_user)
def delete_an_event(request: Request, event_id: int, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' attempting to delete event ID: {event_id}.")
    event_service.delete_event_by_id(db=db, event_id=event_id, user=current_user)
    logger.info(f"Event ID {event_id} deleted by '{current_user.email}'.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)