# src/tasks/utils.py

from . import models as task_models
from src.entities.task import Task as TaskEntity, Priority

def convert_db_task_to_dto(db_task: TaskEntity) -> task_models.Task:
    """
    Bir SQLAlchemy Task nesnesini, bir Pydantic Task DTO'suna dönüştürür.
    """
    return task_models.Task(
        id=db_task.id,
        description=db_task.description,
        is_completed=db_task.is_completed,
        creation_date=db_task.creation_date,
        completion_date=db_task.completion_date,
        due_date=db_task.due_date,
        # priority bir Enum nesnesi olduğu için .value ile int değerini alıyoruz.
        priority=db_task.priority.value if isinstance(db_task.priority, Priority) else db_task.priority,
        owner_id=db_task.owner_id
    )