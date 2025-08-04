# src/entities/task.py - ENUM'LU DOĞRU HALİ

import enum
import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship
from src.database.core import Base


# Python'un standart IntEnum'unu kullanıyoruz.
class Priority(enum.IntEnum):
    Normal = 0  # "Normal" yerine 0
    Low = 1  # "Low" yerine 1
    Medium = 2  # "Medium" yerine 2
    High = 3  # "High" yerine 3
    Top = 4

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    completion_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)

    # SQLAlchemy'ye bu sütunun bir Enum olduğunu ve değerleri sayı olarak saklamasını söylüyoruz.
    priority = Column(SQLAlchemyEnum(Priority), default=Priority.Normal, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")