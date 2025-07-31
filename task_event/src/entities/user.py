# src/entities/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.core import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)

    # Bir kullanıcının birden çok görevi olabilir
    tasks = relationship("Task", back_populates="owner")