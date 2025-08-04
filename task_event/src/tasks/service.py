# src/tasks/service.py

from sqlalchemy.orm import Session

# Kendi modellerimizi ve entity'lerimizi import ediyoruz
from . import models as task_models
from src.entities.task import Task as TaskEntity
from src.entities.user import User as UserEntity


def create_task(db: Session, task: task_models.TaskCreate, owner: UserEntity):
    """
    Yeni bir görev oluşturur ve veritabanına kaydeder.
    - db: Veritabanı oturumu.
    - task: Kullanıcıdan gelen görev bilgileri (Pydantic modeli).
    - owner: Bu görevin sahibi olan, token'dan gelen kullanıcı (SQLAlchemy modeli).
    """

    # 1. Veritabanına kaydedilecek SQLAlchemy Task nesnesini oluşturuyoruz.
    #    **task.model_dump() -> Pydantic modelini bir dictionary'ye çevirir.
    #    **owner_id=owner.id -> Görevin sahibini belirtiriz.
    db_task = TaskEntity(
        **task.model_dump(),
        owner_id=owner.id
    )

    # 2. Standart veritabanı işlemleri
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

# src/tasks/service.py - YENİ EKLENEN FONKSİYON

# ... (create_task fonksiyonu burada bitiyor)

def get_tasks_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    """
    Belirli bir kullanıcıya ait görevleri veritabanından çeker.
    - owner_id: Görevlerin sahibinin kullanıcı ID'si.
    """
    # TaskEntity tablosunu sorgula ve owner_id'si eşleşenleri bul.
    return db.query(TaskEntity).filter(TaskEntity.owner_id == owner_id).offset(skip).limit(limit).all()


def get_task_by_id_and_owner(db: Session, task_id: int, owner_id: int):
    """
    Belirli bir ID'ye sahip ve belirli bir kullanıcıya ait olan tek bir görevi bulur.
    """
    return db.query(TaskEntity).filter(
        TaskEntity.id == task_id,
        TaskEntity.owner_id == owner_id
    ).first()


# src/tasks/service.py - YENİ EKLENEN FONKSİYON

# ... (get_task_by_id_and_owner fonksiyonu burada bitiyor)

def delete_task_by_id_and_owner(db: Session, task_id: int, owner_id: int):
    """
    Belirli bir ID'ye sahip ve belirli bir kullanıcıya ait olan görevi bulur ve siler.
    """
    # 1. Önce, silinecek görevin var olup olmadığını ve bu kullanıcıya ait olup olmadığını bul.
    #    Bunun için daha önce yazdığımız fonksiyonu tekrar kullanabiliriz.
    db_task = get_task_by_id_and_owner(db, task_id=task_id, owner_id=owner_id)

    # 2. Eğer görev bulunamazsa, bir şey yapmadan None döndür.
    if db_task is None:
        return None

    # 3. Eğer görev bulunduysa, onu veritabanından sil ve değişikliği kaydet.
    db.delete(db_task)
    db.commit()

    # 4. Silme işleminin başarılı olduğunu belirtmek için silinen nesneyi geri döndür.
    return db_task


# src/tasks/service.py - YENİ EKLENEN FONKSİYON

# ... (delete_task_by_id_and_owner fonksiyonu burada bitiyor)

def update_task_by_id_and_owner(db: Session, task_id: int, owner_id: int, task_update: task_models.TaskUpdate):
    """
    Belirli bir ID'ye sahip ve belirli bir kullanıcıya ait olan görevi bulur ve günceller.
    """
    # 1. Önce, güncellenecek görevin var olup olmadığını ve bu kullanıcıya ait olup olmadığını bul.
    db_task = get_task_by_id_and_owner(db, task_id=task_id, owner_id=owner_id)

    if db_task is None:
        return None

    # 2. Gelen güncelleme verilerini al. exclude_unset=True, sadece kullanıcı tarafından
    #    gönderilen alanları (None olmayanları) almamızı sağlar.
    update_data = task_update.model_dump(exclude_unset=True)

    # 3. Bulunan veritabanı nesnesinin alanlarını yeni verilerle güncelle.
    for key, value in update_data.items():
        setattr(db_task, key, value)

    # 4. Değişiklikleri veritabanına kaydet.
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task