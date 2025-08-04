# src/tasks/controller.py - DOĞRU VE TAM HALİ

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models as task_models
from . import service as tasks_service
from src.database.dependencies import get_db
from src.auth.service import get_current_user_dependency
from src.users.models import User as UserModel
from fastapi import Response, status

from .models import TaskUpdate

router = APIRouter()

@router.post("/", response_model=task_models.Task, status_code=201)
def create_new_task(
    task: task_models.TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_dependency)
):
    new_task = tasks_service.create_task(db=db, task=task, owner=current_user)
    return new_task

@router.get("/", response_model=List[task_models.Task])
def read_user_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_dependency),
    skip: int = 0,
    limit: int = 100
):
    tasks = tasks_service.get_tasks_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return tasks


# src/tasks/controller.py - YENİ EKLENEN FONKSİYON

# ... (read_user_tasks fonksiyonu burada bitiyor)

@router.get("/{task_id}", response_model=task_models.Task)
def read_single_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user_dependency)
):
    """
    Giriş yapmış kullanıcının, kendisine ait tek bir görevinin detayını getirir.
    - task_id: URL'den gelen görev ID'si.
    """

    # 1. Servis fonksiyonunu çağırarak görevi veritabanından almayı dene.
    db_task = tasks_service.get_task_by_id_and_owner(
        db, task_id=task_id, owner_id=current_user.id
    )

    # 2. Eğer görev bulunamazsa (ya böyle bir görev yoktur ya da görev bu kullanıcıya ait değildir),
    #    bir "Not Found" hatası döndür.
    if db_task is None:
        raise HTTPException(status_code=404, detail="Görev bulunamadı.")

    # 3. Eğer görev bulunduysa, onu geri döndür.
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user_dependency)
):
    """
    Giriş yapmış kullanıcının, kendisine ait tek bir görevini siler.
    """

    # 1. Servis fonksiyonunu çağırarak görevi silmeyi dene.
    deleted_task = tasks_service.delete_task_by_id_and_owner(
        db, task_id=task_id, owner_id=current_user.id
    )

    # 2. Eğer servis fonksiyonu None döndürürse (görev bulunamadıysa),
    #    bir "Not Found" hatası döndür.
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Görev bulunamadı.")

    # 3. Eğer silme başarılıysa, HTTP standardına uygun olarak,
    #    içeriği olmayan bir 204 cevabı döndür.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# src/tasks/controller.py - YENİ EKLENEN FONKSİYON

# ... (delete_single_task fonksiyonu burada bitiyor)

@router.put(path="/update", response_model=task_models.Task)
def update_single_task(
        task_update: task_models.TaskUpdate,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user_dependency)
):
    """
    Giriş yapmış kullanıcının, kendisine ait tek bir görevini günceller.
    """

    updated_task = tasks_service.update_task_by_id_and_owner(
        db, task_id=task_update.task_id, owner_id=current_user.id, task_update=task_update

    )

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Görev bulunamadı.")

    return updated_task


@router.get("/update/{task_id}", response_model=task_models.Task)
def read_single_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user_dependency)
):
    """
    Giriş yapmış kullanıcının, kendisine ait tek bir görevinin detayını getirir.
    - task_id: URL'den gelen görev ID'si.
    """
    task_update=TaskUpdate()
    task_update.description="Güncellendi"
    task_update.priority=2
    updated_task = tasks_service.update_task_by_id_and_owner(
        db, task_id=task_id, owner_id=current_user.id, task_update=task_update

    )

    # 3. Eğer görev bulunduysa, onu geri döndür.
    return updated_task