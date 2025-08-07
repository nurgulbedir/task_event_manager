# src/tasks/controller.py - TAM VE NİHAİ HALİ

from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from sqlalchemy.orm import Session
from typing import List

# --- Proje İçi Gerekli Modüller ---
from . import models as task_models
from . import service as tasks_service
from src.database.dependencies import get_db
from src.auth.service import get_current_user_dependency
from src.entities.user import User as UserEntity
from src.logger import get_logger
from src.rate_limiter import limiter, get_token_user

# --- Logger'ı Başlatma ---
logger = get_logger(__name__)
router = APIRouter()

@router.post("/", response_model=task_models.Task, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/hour", key_func=get_token_user)
def create_new_task(request: Request, task: task_models.TaskCreate, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' is creating a new task.")
    return tasks_service.create_task(db=db, task=task, owner=current_user)

@router.get("/", response_model=List[task_models.Task])
@limiter.limit("100/hour", key_func=get_token_user)
def read_user_tasks(request: Request, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency), skip: int = 0, limit: int = 100):
    logger.info(f"User '{current_user.email}' requested their tasks. Skip: {skip}, Limit: {limit}.")
    return tasks_service.get_tasks_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=task_models.Task)
@limiter.limit("100/hour", key_func=get_token_user)
def read_single_task(request: Request, task_id: int, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' requested details for task ID: {task_id}.")
    db_task = tasks_service.get_task_by_id_and_owner(db, task_id=task_id, owner_id=current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Görev bulunamadı.")
    return db_task

@router.put("/{task_id}", response_model=task_models.Task)
@limiter.limit("100/hour", key_func=get_token_user)
def update_single_task(request: Request, task_id: int, task_update: task_models.TaskUpdate, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' is attempting to update task ID: {task_id}.")
    updated_task = tasks_service.update_task_by_id_and_owner(db, task_id=task_id, owner_id=current_user.id, task_update=task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Görev bulunamadı.")
    logger.info(f"Task ID {task_id} was successfully updated by user '{current_user.email}'.")
    return updated_task

@router.patch("/{task_id}/complete", response_model=task_models.Task)
@limiter.limit("100/hour", key_func=get_token_user)
def mark_task_complete(request: Request, task_id: int, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' is marking task ID: {task_id} as complete.")
    completed_task = tasks_service.mark_task_as_complete(db, task_id=task_id, owner_id=current_user.id)
    if completed_task is None:
        raise HTTPException(status_code=404, detail="Görev bulunamadı.")
    logger.info(f"Task ID {task_id} was successfully marked as complete by user '{current_user.email}'.")
    return completed_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("100/hour", key_func=get_token_user)
def delete_single_task(request: Request, task_id: int, db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_dependency)):
    logger.info(f"User '{current_user.email}' is attempting to delete task ID: {task_id}.")
    was_deleted = tasks_service.delete_task_by_id_and_owner(db, task_id=task_id, owner_id=current_user.id)
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Görev bulunamadı.")
    logger.info(f"Task ID {task_id} was successfully deleted by user '{current_user.email}'.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)