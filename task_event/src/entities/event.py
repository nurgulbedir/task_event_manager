# src/entities/event.py

import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Etkinliği kimin oluşturduğunu belirtir.
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User") # 'User' modeline bir referans

    # Bir etkinliğin birden çok katılımcısı olabilir.
    participants = relationship("EventParticipant", back_populates="event", cascade="all, delete-orphan")