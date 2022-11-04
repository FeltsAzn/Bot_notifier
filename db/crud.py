# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
from models import User, Services


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
database_url = os.getenv("DATABASE_URL")


class Database:

    @staticmethod
    def create_session():
        engine = create_engine(database_url, future=True, echo=True)
        session = sessionmaker(engine, expire_on_commit=False)
        return session

    def create_user(self, tg_id: int, name: str) -> bool | Exception:
        database_session = self.create_session()
        with database_session() as session:
            data = User(
                user_id=tg_id,
                username=name)
            try:
                session.add(data)
            except Exception as ex:
                session.rollback()
                # logger info
                return ex
            else:
                session.commit()
                return True

    def create_service(self, name: str) -> bool | Exception:
        database_session = self.create_session()
        with database_session() as session:
            data = Services(service_name=name)
            try:
                session.add(data)
            except Exception as ex:
                session.rollback()
                # logger info
                return ex
            else:
                session.commit()
                return True

    def get_users(self) -> list[tuple]:
        database_session = self.create_session()
        with database_session() as session:
            data = session.query(User.user_id, User.username)
            users = []
            for tg_id, name in data:
                users.append((tg_id, name))
            return users

    def get_services(self) -> list[any]:
        database_session = self.create_session()
        with database_session() as session:
            data = session.query(Services.service_name)
            services = []
            for name in data:
                services.append(name)
            return services

