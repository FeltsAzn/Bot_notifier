from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.models import User
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
database_url_async = os.getenv("DATABASE_URL_ASYNC")
database_url = os.getenv("DATABASE_URL")


class Database:

    @staticmethod
    async def create_session():
        """Асинхронная сессия подключения к бд"""
        engine = create_async_engine(database_url_async, future=True, echo=True)
        session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        return session

    async def create_user(self, tg_id: int, name: str) -> bool:
        """Создание нового пользователя"""
        database_session = await self.create_session()
        async with database_session() as session:
            data = User(
                user_id=tg_id,
                username=name)
            try:
                session.add(data)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                # TODO сделать перенаправление вывод бд в логгер
                # logger warning(IntegrityError)
                return True
            except Exception as ex:
                await session.rollback()
                # logger error()
                return False

    async def delete_user(self, tg_id: int) -> bool:
        """Удаление пользователя"""
        database_session = await self.create_session()
        async with database_session() as session:
            try:
                query = select(User).where(User.user_id == tg_id)
                database_response = await session.execute(query)
                user = database_response.scalar()

                await session.delete(user)
                await session.commit()
                return True
            except Exception as ex:
                await session.rollback()
                # TODO сделать перенаправление вывод бд в логгер
                # logger error()
                return False

    async def get_user(self, tg_id: int) -> tuple | bool:
        """Список всех пользователей"""
        database_session = await self.create_session()
        async with database_session() as session:
            try:
                query = select(User).where(User.user_id == tg_id)
                database_response = await session.execute(query)
                user = database_response.one()
                user: tuple = tuple(map(lambda x: (x.user_id, x.username, x.notification), user))
                return user[0]
            except Exception as ex:
                # log.warning(ex)
                return False

    async def get_all_users(self) -> list[tuple] | bool:
        """Список всех пользователей"""
        database_session = await self.create_session()
        async with database_session() as session:
            try:
                query = select(User)
                database_response = await session.execute(query)
                user = database_response.scalars()
                users = list(map(lambda x: (x.user_id, x.username, x.notification), user))
                return users
            except Exception as ex:
                # log.warning(ex)
                return False

    async def active_notification(self, tg_id) -> bool:
        """Активация уведомлений пользователя"""
        database_session = await self.create_session()
        async with database_session() as session:
            try:
                query = select(User).where(User.user_id == tg_id)
                database_response = await session.execute(query)
                user = database_response.scalar()
                user.notification = "ACTIVATED"
                await session.commit()
                return True
            except Exception as ex:
                # log.warning(ex)
                return False

    async def deactivated_notification(self, tg_id) -> bool:
        """Деактивация уведомлений пользователя"""
        database_session = await self.create_session()
        async with database_session() as session:
            try:
                query = select(User).where(User.user_id == tg_id)
                database_response = await session.execute(query)
                user = database_response.scalar()
                user.notification = "DEACTIVATED"
                await session.commit()
                return True
            except Exception as ex:
                # log.warning(ex)
                return False

    async def notifications_state(self) -> list[tuple] | bool:
        """Состояние уведомлений пользователя"""
        database_session = await self.create_session()
        async with database_session() as session:
            try:
                query = select(User)
                database_response = await session.execute(query)
                user = database_response.scalars()
                users = list(map(lambda x: (x.user_id, x.notification), user))
                return users
            except Exception as ex:
                # log.warning(ex)
                return False

    @staticmethod
    def create_sync_session():
        """Синхронная сессия подключения к бд"""
        engine = create_engine(database_url, future=True, echo=True)
        session = sessionmaker(engine, expire_on_commit=False)
        return session

    def get_users_sync(self) -> list[tuple] | bool:
        """Синхронный обработчик дял получение списка пользователей"""
        database_session = self.create_sync_session()
        with database_session() as session:
            try:
                query = select(User)
                database_response = session.execute(query)
                user = database_response.scalars()
                users = list(map(lambda x: (x.user_id, x.username, x.notification), user))
                return users
            except Exception as ex:
                # log.warning(ex)
                print("ERROR")
                return False
