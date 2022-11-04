from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
import os
from dotenv import load_dotenv


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)


class Services(Base):
    __tablename__ = 'Services'

    id = Column(Integer, primary_key=True)
    service_name = Column(String)


if __name__ == '__main__':
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    database_url = os.getenv("DATABASE_URL")

    create_eng = create_engine(database_url, future=True, echo=True)
    Base.metadata.create_all(create_eng)



