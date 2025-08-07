# src/users/utils.py

from . import models as user_models
from src.entities.user import User as UserEntity

def convert_db_user_to_dto(db_user: UserEntity) -> user_models.User:
    """
    Bir SQLAlchemy User nesnesini, bir Pydantic User DTO'suna dönüştürür.
    Bu DTO, parola gibi hassas bilgileri içermez.
    """
    return user_models.User(
        id=db_user.id,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name
    )