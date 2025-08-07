# src/entities/event_participant.py - GÜNCELLENMİŞ HALİ

import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from src.database.core import Base


class ResponseStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    TENTATIVE = "tentative"


class EventParticipant(Base):
    __tablename__ = "event_participants"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLAlchemyEnum(ResponseStatus), default=ResponseStatus.PENDING, nullable=False)

    # Bu kaydın hangi etkinliğe ait olduğunu belirtir.
    # 'Event' modelindeki 'participants'a geri bağlanır.
    event = relationship("Event", back_populates="participants")

    # Bu kaydın hangi kullanıcıya ait olduğunu belirtir.
    # 'User' modelindeki 'event_participations'a geri bağlanır.
    user = relationship("User", back_populates="event_participations")