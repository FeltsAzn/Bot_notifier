from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

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
