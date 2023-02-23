import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv


"""
Файл create_database.py - создание новой базы данных для приложения бота, если будет удалена активная база
"""

dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
Base = declarative_base()
database_url = os.getenv("DATABASE_URL")


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    notification = Column(String, default="ACTIVATED")
    access = Column(String, default="USER")


def create_new_database():
    logs_path = os.path.join(os.path.dirname(__file__), "info.db")
    if not os.path.exists(logs_path):
        eng = create_engine(database_url, future=True, echo=True)
        Base.metadata.create_all(eng)
    else:
        print("Database created already")


create_new_database()