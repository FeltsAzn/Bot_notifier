import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://bot:mongo_password@localhost:27017/"

client = AsyncIOMotorClient(MONGO_URL)

database = client["bot_users"]


async def create_data(db):
    await db.users.insert_one({"user": "name"})


asyncio.run(create_data(database))