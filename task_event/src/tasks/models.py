# src/tasks/models.py - EN TEMİZ HALİ

from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    description: str | None = None
    priority: int | None = None
    due_date: datetime | None = None
    is_completed: bool | None = None

class TaskCreate(TaskBase):
    description: str # Yeni görevde açıklama zorunlu
    priority: int = 0 # Varsayılan değer

class TaskUpdate(TaskBase):
    pass # TaskBase ile aynı, tüm alanlar opsiyonel

class Task(TaskBase):
    id: int
    owner_id: int
    creation_date: datetime

    class Config:
        from_attributes = True