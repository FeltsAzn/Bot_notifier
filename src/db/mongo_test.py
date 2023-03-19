import asyncio
import functools
from utils.logger import logger
from motor.motor_asyncio import AsyncIOMotorClient


# TODO: connect to mongo db
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
                "ban_list": {
                    "quote": [],
                    "time_alive": 0
                }
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
    async def get_user(self, tg_id: int) -> dict:
        user = await self.USERS.find_one({"tg_id": tg_id})
        if user:
            return user
        logger.exception(f"User {tg_id} not found in database")
        return user

    @exception_middleware
    async def get_users(self) -> list[dict]:
        users_set = []
        users = self.USERS.find()
        for user in await users.to_list(length=100):
            users_set.append(user)
        if not users_set:
            logger.exception("User list is empty")
        return users_set


    @exception_middleware
    async def activate_notification(self, tg_id) -> bool:
        user = await self.USERS.find_one_and_update({"tg_id": tg_id, "notify": False})
        return user

    @exception_middleware
    async def deactivate_notification(self, tg_id) -> bool:
        user = await self.USERS.find_one_and_update({"tg_id": tg_id}, {"$notify": False})
        return user



async def db_methods():
    database = Database()
    await database.create_user(4586546, "Nik")
    await database.create_user(4899416, "Rom")
    await database.create_user(4854526, "Tim")
    await database.create_user(4488551, "Aza")
    await database.create_user(8498494, "Lil")
    # resp = await database.delete_user(4586546)
    # print(resp)
    # resp = await database.get_user(4586546)
    resp = await database.get_users()
    print(resp)
    resp = await database.deactivate_notification(8498494)
    print(resp)


asyncio.run(db_methods())
