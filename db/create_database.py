import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv


"""
Файл create_database.py - создание новой базы данных для приложения бота, если будет удалена активная база
"""


Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    notification = Column(String, default="ACTIVATED")
    access = Column(String, default="USER")


async def create():
    dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    database_url = os.getenv("DATABASE_URL_ASYNC")
    print(database_url)

    eng = create_async_engine(database_url, future=True, echo=True)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create())
