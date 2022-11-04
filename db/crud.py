from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from db.models import User, Services


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
database_url = os.getenv("DATABASE_URL")


class Database:

    @staticmethod
    async def create_session():
        engine = create_async_engine(database_url, future=True, echo=True)
        session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        return session

    async def create_user(self, tg_id: int, name: str) -> bool | Exception:
        database_session = await self.create_session()
        async with database_session() as session:
            data = User(
                user_id=tg_id,
                username=name)
            try:
                session.add(data)
            except Exception as ex:
                await session.rollback()
                # logger info
                return ex
            else:
                await session.commit()
                return True

    async def create_service(self, name: str) -> bool | Exception:
        database_session = await self.create_session()
        async with database_session() as session:
            data = Services(service_name=name)
            try:
                session.add(data)
            except Exception as ex:
                await session.rollback()
                # logger info
                return ex
            else:
                await session.commit()
                return True

    async def get_users(self) -> list[tuple]:
        database_session = await self.create_session()
        async with database_session() as session:
            data = await session.query(User.user_id, User.username)
            users = []
            for tg_id, name in data:
                users.append((tg_id, name))
            return users

    async def get_services(self) -> list[any]:
        database_session = await self.create_session()
        async with database_session() as session:
            data = await session.query(Services.service_name)
            services = []
            for name in data:
                services.append(name)
            return services

