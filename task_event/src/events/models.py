# src/events/models.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from src.entities.event_participant import ResponseStatus

# --- Katılımcı Modelleri ---

# API'den yanıt dönerken bir katılımcının nasıl görüneceğini belirler
class EventParticipantResponse(BaseModel):
    user_id: int
    user_email: EmailStr # Kolaylık olması için email'i de ekleyelim
    status: ResponseStatus

    class Config:
        from_attributes = True


# --- Etkinlik Modelleri (DTOs) ---

# Bir etkinlik oluşturulurken API'ye gönderilecek temel veriler
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    # Etkinlik oluşturulurken doğrudan davet edilecek kullanıcıların e-postaları
    invitee_emails: Optional[List[EmailStr]] = []


# Bir etkinliği güncellerken kullanılacak model (tüm alanlar opsiyonel)
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


# API'den tam bir etkinlik verisi dönerken kullanılacak model
class Event(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    creation_date: datetime
    creator_id: int
    # İç içe model kullanarak katılımcıları da yanıtta gösteriyoruz
    participants: List[EventParticipantResponse] = []

    class Config:
        from_attributes = True

# --- Davet Yanıtlama Modeli ---
class EventInvitationUpdate(BaseModel):
    status: ResponseStatus # Kullanıcı sadece kendi durumunu güncelleyebilir