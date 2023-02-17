from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select

from db.models import User
from logger import logger
import os

"""
Файл crud.py - методы для создания, чтения, удаления и обновления полей в бд
"""

database_url_async = os.getenv("DATABASE_URL_ASYNC")
database_url = os.getenv("DATABASE_URL")


class Database:

    @staticmethod
    async def create_session():
        """Асинхронная сессия подключения к бд"""
        try:
            engine = create_async_engine(database_url_async, future=True, echo=False)
            session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
            return session
        except Exception as ex:
            logger.exception(f"Asynchronous session maker error: {ex}")
            return False

    async def create_user(self, tg_id: int, name: str) -> bool:
        """Создание нового пользователя"""
        database_session = await self.create_session()
        if database_session:
            async with database_session() as session:
                data = User(
                    user_id=tg_id,
                    username=name)
                try:
                    session.add(data)
                    await session.commit()
                    logger.info(f"Create new user with tg id: {tg_id}")
                    return True
                except IntegrityError:
                    await session.rollback()
                    logger.info(f"Not unique telegram id, return old-created user")
                    return True
                except Exception as ex:
                    await session.rollback()
                    logger.exception(f"Database exception on create user to db with tg_id: {tg_id}\n"
                                     f"exception type {type(ex)} - {ex}")
                    return False
        return False

    async def delete_user(self, tg_id: int) -> bool:
        """Удаление пользователя"""
        database_session = await self.create_session()
        if database_session:
            async with database_session() as session:
                try:
                    query = select(User).where(User.user_id == tg_id)
                    database_response = await session.execute(query)
                    user = database_response.scalar()

                    await session.delete(user)
                    await session.commit()

                    logger.info(f"Delete user with tg id: {tg_id}")
                    return True
                except Exception as ex:
                    await session.rollback()
                    logger.exception(f"Exception on delete user on db with tg_id: {tg_id}\n"
                                     f"exception type {type(ex)} - {ex}")
                    return False
        return False

    async def get_user(self, tg_id: int) -> tuple | bool:
        """Список всех пользователей(Синхронно, используется для старта приложения)"""
        database_session = await self.create_session()
        if database_session:
            async with database_session() as session:
                try:
                    query = select(User).where(User.user_id == tg_id)
                    database_response = await session.execute(query)
                    user = database_response.one()
                    user: tuple = tuple(map(lambda x: (x.user_id, x.username, x.notification, x.access), user))
                    return user[0]
                except Exception as ex:
                    logger.exception(f"Exception in asynchronous get user on db with tg id: {tg_id}\n"
                                     f"exception type {type(ex)} - {ex}")
                    return ()
        return False

    async def async_get_users(self) -> list[tuple] | bool:
        """Список всех пользователей (асинхронно, используется во время работы программы)"""
        database_session = await self.create_session()
        if database_session:
            async with database_session() as session:
                try:
                    query = select(User)
                    database_response = await session.execute(query)
                    user = database_response.scalars()
                    users = list(map(lambda x: (x.user_id, x.username, x.notification, x.access), user))
                    return users
                except Exception as ex:
                    logger.exception(f"Exception in asynchronous get all users on db\n"
                                     f"exception type {type(ex)} - {ex}")
                    return []
        return False

    async def active_notification(self, tg_id) -> bool:
        """Активация уведомлений пользователя"""
        database_session = await self.create_session()
        if database_session:
            async with database_session() as session:
                try:
                    query = select(User).where(User.user_id == tg_id)
                    database_response = await session.execute(query)
                    user = database_response.scalar()
                    user.notification = "ACTIVATED"
                    await session.commit()
                    logger.info(f"Activate notifications for tg id: {tg_id}")
                    return True
                except Exception as ex:
                    logger.exception(f"Exception in activate notifications with tg id: {tg_id}\n"
                                     f"exception type {type(ex)} - {ex}")
                    return False
        return False

    async def deactivated_notification(self, tg_id) -> bool:
        """Деактивация уведомлений пользователя"""
        database_session = await self.create_session()
        if database_session:
            async with database_session() as session:
                try:
                    query = select(User).where(User.user_id == tg_id)
                    database_response = await session.execute(query)
                    user = database_response.scalar()
                    user.notification = "DEACTIVATED"
                    await session.commit()
                    logger.info(f"Deactivate notifications for tg id: {tg_id}")
                    return True
                except Exception as ex:
                    logger.exception(f"Exception in deactivate notifications with tg id: {tg_id}\n"
                                     f"exception type {type(ex)} - {ex}")
                    return False
        return False

    async def notifications_state(self) -> list[tuple] | bool:
        """Состояние уведомлений пользователя"""
        database_session = await self.create_session()
        if database_session:
            async with database_session() as session:
                try:
                    query = select(User)
                    database_response = await session.execute(query)
                    user = database_response.scalars()
                    users = list(map(lambda x: (x.user_id, x.notification), user))
                    return users
                except Exception as ex:
                    logger.exception(f"Exception in asynchronous notifications state on db\n"
                                     f"exception type {type(ex)} - {ex}")
                    return False
        return False

    @staticmethod
    def create_sync_session():
        """Синхронная сессия подключения к бд"""
        try:
            engine = create_engine(database_url, future=True, echo=True)
            session = sessionmaker(engine, expire_on_commit=False)
            return session
        except Exception as ex:
            logger.exception(f"Synchronous session maker error: {ex}")
            return False

    def sync_get_users(self) -> list[tuple] | bool:
        """Синхронный обработчик для получение списка пользователей (для корректного старта приложения)"""
        database_session = self.create_sync_session()
        if database_session:
            with database_session() as session:
                try:
                    query = select(User)
                    database_response = session.execute(query)
                    user = database_response.scalars()
                    users = list(map(lambda x: (x.user_id, x.username, x.notification, x.access), user))
                    return users
                except Exception as ex:
                    logger.exception(f"Exception in synchronous get all users on db\n"
                                     f"exception type {type(ex)} - {ex}")
                    return False
        return False
