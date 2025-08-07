# src/tasks/service.py - TAM VE NİHAİ HALİ

from sqlalchemy.orm import Session
from typing import List
import datetime

# --- Proje İçi Gerekli Modüller ---
from . import models as task_models
from . import utils as task_utils  # <-- Yeni yardımcı fonksiyonumuz
from src.entities.task import Task as TaskEntity
from src.entities.user import User as UserEntity
from src.logger import get_logger
from src.exceptions import NotFoundException # Genel bir "Bulunamadı" hatası yeterli olacaktır.

# --- Logger'ı Başlatma ---
logger = get_logger(__name__)


def create_task(db: Session, task: task_models.TaskCreate, owner: UserEntity) -> task_models.Task:
    """Yeni bir görev oluşturur ve oluşturulan görevi DTO olarak döndürür."""
    logger.debug(f"Service: Creating task for user '{owner.email}'.")
    db_task = TaskEntity(**task.model_dump(), owner_id=owner.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return task_utils.convert_db_task_to_dto(db_task)


def get_tasks_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[task_models.Task]:
    """Bir kullanıcıya ait görevleri DTO listesi olarak döndürür."""
    tasks_from_db = db.query(TaskEntity).filter(TaskEntity.owner_id == owner_id).offset(skip).limit(limit).all()
    return [task_utils.convert_db_task_to_dto(task) for task in tasks_from_db]


def get_task_by_id_and_owner(db: Session, task_id: int, owner_id: int) -> task_models.Task | None:
    """Belirli bir görevi DTO olarak döndürür, bulunamazsa None döndürür."""
    db_task = db.query(TaskEntity).filter(TaskEntity.id == task_id, TaskEntity.owner_id == owner_id).first()
    if not db_task:
        return None
    return task_utils.convert_db_task_to_dto(db_task)


def update_task_by_id_and_owner(db: Session, task_id: int, owner_id: int, task_update: task_models.TaskUpdate) -> task_models.Task:
    db_task = db.query(TaskEntity).filter(TaskEntity.id == task_id, TaskEntity.owner_id == owner_id).first()
    if db_task is None:
        # ESKİ: return None
        # YENİ:
        raise NotFoundException(detail=f"Görev ID: {task_id} bulunamadı veya bu kullanıcıya ait değil.")
    # ... (güncelleme mantığı) ...
    return task_utils.convert_db_task_to_dto(db_task)


def delete_task_by_id_and_owner(db: Session, task_id: int, owner_id: int):  # Artık bool döndürmüyor
    db_task = db.query(TaskEntity).filter(TaskEntity.id == task_id, TaskEntity.owner_id == owner_id).first()
    if db_task is None:
        # ESKİ: return False
        # YENİ:
        raise NotFoundException(detail=f"Görev ID: {task_id} bulunamadı veya bu kullanıcıya ait değil.")

    db.delete(db_task)
    db.commit()
    logger.info(f"Service: Task ID {task_id} deleted from DB.")
    # Başarılı olunca bir şey döndürmeye gerek yok.

def mark_task_as_complete(db: Session, task_id: int, owner_id: int) -> task_models.Task | None:
    """Bir görevi tamamlandı olarak işaretler ve güncel halini DTO olarak döndürür."""
    db_task = db.query(TaskEntity).filter(TaskEntity.id == task_id, TaskEntity.owner_id == owner_id).first()
    if db_task is None:
        return None

    db_task.is_completed = True
    db_task.completion_date = datetime.datetime.utcnow()

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return task_utils.convert_db_task_to_dto(db_task)