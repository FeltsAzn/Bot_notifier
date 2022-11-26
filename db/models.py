from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


"""
Файл models.py - шаблон таблицы для бд. На основании этого шаблона вносятся и читаются данные из бд
"""

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    notification = Column(String, default="ACTIVATED")
    access = Column(String, default="USER")
