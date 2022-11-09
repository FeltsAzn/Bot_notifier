from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    notification = Column(String, default='ACTIVATED')
    access = Column(String, default='USER')
