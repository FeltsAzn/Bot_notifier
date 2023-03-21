import functools
from db.models import User
from utils.logger import logger
from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    MONGO_URL = "mongodb://bot:mongo_password@localhost:27017/"
    client = AsyncIOMotorClient(MONGO_URL)
    DB = client["bot_users"]
    USERS = DB.users

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
    async def create_user(self, tg_id: int, name: str) -> bool | None:
        """Создание нового пользователя"""
        is_exist_user = await self.USERS.find_one({"tg_id": tg_id})
        if not is_exist_user:
            data = {
                "tg_id": tg_id,
                "username": name,
                "access": "USER",
                "notify": True,
                "ban_list": [
                    {
                        "quote": "",
                        "time_alive": 0
                    }
                ]
            }
            response = await self.USERS.insert_one(data)
            if response.acknowledged:
                logger.info(f"User {tg_id}@{name} created successfully")
                return True
            logger.exception(f"User {tg_id}@{name} not created. Unexpect error.")
            return False
        logger.info(f"User {tg_id} is exist already")
        return None

    @exception_middleware
    async def delete_user(self, tg_id: int) -> bool | None:
        response = await self.USERS.find_one_and_delete({"tg_id": tg_id})
        if response:
            logger.info(f"User {tg_id} deleted successfully")
            return True
        logger.exception(f"User {tg_id} not deleted. Unexpect error.")
        return False

    @exception_middleware
    async def change_user_access(self, tg_id: int, access: str) -> bool:
        response = await self.USERS.find_one_and_update({"tg_id": tg_id}, {"$set": {"access": access}})
        if response:
            logger.info(f"User: {tg_id} access: {access} changed successfully")
            return True
        logger.exception(f"User {tg_id} not found in database. ")
        return False

    @exception_middleware
    async def get_users(self) -> list[User]:
        users_set = []
        users = self.USERS.find()
        for user in await users.to_list(length=100):
            users_set.append(User(user))
        if not users_set:
            logger.exception("User list is empty")
        return users_set

    @exception_middleware
    async def activate_notification(self, tg_id) -> bool:
        response = await self.USERS.find_one_and_update({"tg_id": tg_id}, {"$set": {"notify": True}})
        if response:
            logger.info(f"Activate notifications for tg id: {tg_id}")
            return True
        logger.exception(f"User {tg_id} not found in database")
        return False

    @exception_middleware
    async def deactivate_notification(self, tg_id) -> bool:
        response = await self.USERS.find_one_and_update({"tg_id": tg_id}, {"$set": {"notify": False}})
        if response:
            logger.info(f"Deactivate notifications for tg id: {tg_id}")
            return True
        logger.exception(f"User {tg_id} not found in database")
        return False
