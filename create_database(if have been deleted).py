from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
import os
from dotenv import load_dotenv
import asyncio


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)


class Services(Base):
    __tablename__ = 'Services'

    id = Column(Integer, primary_key=True)
    service_name = Column(String)


async def create():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    database_url = os.getenv("DATABASE_URL")
    print(database_url)

    eng = create_async_engine(database_url, future=True, echo=True)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create())
