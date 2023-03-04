import functools
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from load_virtual_variables import DATABASE_ASYNC_URL
from db.models import User
from logger import logger


# TODO: connect to mongo db
class Database:
    ENGINE = create_async_engine(DATABASE_ASYNC_URL, future=True, echo=False)
    ASYNC_SESSION = sessionmaker(ENGINE, expire_on_commit=False, class_=AsyncSession)

    @staticmethod
    def exception_middleware(func):
        @functools.wraps(func)
        async def wrap(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as ex:
                logger.exception(f"Database is not exist. Or {type(ex)}: {ex}\n"
                                 f"arguments: {args} and keywords: {kwargs}")
                raise SystemExit
        return wrap

    @exception_middleware
    async def create_user(self, tg_id: int, name: str) -> bool:
        """Создание нового пользователя"""
        async with self.ASYNC_SESSION() as session:
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

    @exception_middleware
    async def delete_user(self, tg_id: int) -> bool:
        """Удаление пользователя"""
        async with self.ASYNC_SESSION() as session:
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

    @exception_middleware
    async def get_user(self, tg_id: int) -> dict:
        """Get one user"""
        async with self.ASYNC_SESSION() as session:
            try:
                query = select(User).where(User.user_id == tg_id)
                database_response = await session.execute(query)
                user = database_response.one()
                users = {x.user_id: {"username": x.username, "state": x.notification, "access": x.access} for x in user}
                return users
            except Exception as ex:
                logger.exception(f"Exception in asynchronous get user on db with tg id: {tg_id}\n"
                                 f"exception type {type(ex)} - {ex}")
                return {}

    @exception_middleware
    async def async_get_users(self) -> dict:
        """Список всех пользователей (асинхронно, используется во время работы программы)"""
        async with self.ASYNC_SESSION() as session:
            try:
                query = select(User)
                database_response = await session.execute(query)
                user = database_response.scalars()
                users = {x.user_id: {"username": x.username, "state": x.notification, "access": x.access} for x in user}
                return users
            except Exception as ex:
                logger.exception(f"Exception in asynchronous get all users on db\n"
                                 f"exception type {type(ex)} - {ex}")
                return {}

    @exception_middleware
    async def activate_notification(self, tg_id) -> bool:
        """Активация уведомлений пользователя"""
        async with self.ASYNC_SESSION() as session:
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

    @exception_middleware
    async def deactivate_notification(self, tg_id) -> bool:
        """Деактивация уведомлений пользователя"""
        async with self.ASYNC_SESSION() as session:
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
