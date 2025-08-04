# src/tasks/models.py - ENUM'LU DOĞRU HALİ

from pydantic import BaseModel
from datetime import datetime
import enum # Python'un standart enum'u

# entities'deki Enum tanımının BİREBİR AYNISI
class Priority(enum.IntEnum):
    Normal = 0
    Low = 1
    Medium = 2
    High = 3
    Top = 4

class TaskCreate(BaseModel):
    description: str
    due_date: datetime | None = None
    priority: Priority = Priority.Normal

class Task(BaseModel):
    id: int
    description: str
    is_completed: bool
    creation_date: datetime
    due_date: datetime
    priority: Priority # Pydantic, cevabı dönerken sayıyı Enum üyesine çevirecek
    owner_id: int

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    description: str | None = None
    task_id:int | None = None
    due_date: datetime
    priority: int | None = None
    is_completed: bool
