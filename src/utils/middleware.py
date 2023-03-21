from typing import Callable
from db.mongodb import Database
from utils.virtual_variables import REDIS_ASYNC_CONN, LOAD_SETTINGS, MAIN_ADMIN
from utils.logger import logger
import functools

"""
The middleware.py file is designed to hide database calls and filter data when a response is received.
from the database for readability of the code.
"""
db = Database()


def validate_user(func) -> Callable:
    @functools.wraps(func)
    async def wrap(message, state=None) -> Callable:
        async with REDIS_ASYNC_CONN as redis_connection:
            user_cache = await redis_connection.get_value("users_list")
        if f"{message.from_user.id}" in user_cache:
            return await func(message, True, state)
        return await func(message, False, state)

    return wrap


def admin_validator(func) -> Callable:
    @functools.wraps(func)
    async def wrap(message) -> Callable:
        admins = await get_admins()
        if message.from_user.id == MAIN_ADMIN:
            return await func(message)

        if f"{message.from_user.id}" in admins:
            return await func(message)
    return wrap


async def change_access(tg_id: int, access: str) -> bool:
    response: bool = await db.change_user_access(tg_id=tg_id, access=access)
    if response:
        await update_users_list()
        return response
    return response


async def update_users_list() -> None:
    """Update list of users for notification list in one thread mod"""
    async with REDIS_ASYNC_CONN as redis_connection:
        all_users: list = await db.get_users()
        users = {}
        for user in all_users:
            await redis_connection.update_exist_key(user.tg_id, user.info)
            users[user.tg_id] = user.info
        await redis_connection.update_exist_key("users_list", users)


async def create_new_user(tg_id: int, username: str) -> bool:
    """Creating new user"""
    user_is_registered = await db.create_user(tg_id=tg_id, name=username)
    if user_is_registered:
        await update_users_list()
        return user_is_registered
    return user_is_registered


async def get_admins() -> dict:
    """Update admin list for app in running"""
    async with REDIS_ASYNC_CONN as redis_connection:
        all_users = await redis_connection.get_value("users_list")
    only_admins = {tg_id: data for tg_id, data in all_users.items() if data["access"] == "ADMIN"}
    return only_admins


async def get_all_users() -> dict:
    """Update user list for admin panel if app has been running for a while"""
    async with REDIS_ASYNC_CONN as redis_connection:
        return await redis_connection.get_value("users_list")


async def delete_user_from_tg_id(user_tg_id: int) -> bool:
    """Deleting user by tg id"""
    is_deleted = await db.delete_user(user_tg_id)
    if is_deleted:
        await update_users_list()
        return is_deleted
    return is_deleted


async def get_user_from_tg_id(user_tg_id: int) -> dict:
    """Receiving user by tg id"""
    async with REDIS_ASYNC_CONN as redis_connection:
        return await redis_connection.get_value(f"{user_tg_id}")


async def activate_notify(tg_id: int) -> bool:
    """Activation notifications on user"""
    is_activated = await db.activate_notification(tg_id)
    if is_activated:
        await update_users_list()
        return is_activated
    return is_activated


async def deactivate_notify(tg_id: int) -> bool:
    """Deactivation notifications on user"""
    is_deactivated = await db.deactivate_notification(tg_id)
    if is_deactivated:
        await update_users_list()
        return is_deactivated
    return is_deactivated


async def set_value_to_redis(category: str, value: str) -> bool:
    try:
        value = float(value)
        settings = await get_settings()
    except ValueError:
        return False
    else:
        settings[category] = value
        async with LOAD_SETTINGS as session:
            await session.create_key_and_value("SETTINGS", settings)
        logger.info(f"Settings updated category '{category}' value: '{value}'. All settings: {settings}")
        return True


async def get_settings() -> dict:
    async with LOAD_SETTINGS as session:
        settings = await session.get_value("SETTINGS")
    return settings
