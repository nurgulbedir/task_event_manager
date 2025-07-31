# src/entities/task.py
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.database.core import Base
import datetime


class Priority(enum.Enum):
    Normal = 0
    Low = 1
    Medium = 2
    High = 3
    Top = 4


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    completion_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Enum(Priority), default=Priority.Normal)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")


  #Not: `ForeignKey("users.id")`ile bu tablonun `users` tablosuna `id` alanı üzerinden bağlı olduğunu belirttik.