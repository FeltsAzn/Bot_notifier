from typing import Callable
from db.crud import Database
from utils.virtual_variables import REDIS_ASYNC_CONN
import functools

"""
The middleware.py file is designed to hide database calls and filter data when a response is received.
from the database for readability of the code.
"""


def validate_user(func) -> Callable:
    @functools.wraps(func)
    async def wrap(message) -> Callable:
        async with REDIS_ASYNC_CONN as redis_connection:
            user_cache = await redis_connection.get_value("users_list")
        if f"{message.from_user.id}" in user_cache:
            return await func(message, True)
        return await func(message, False)

    return wrap


def admin_validator(func) -> Callable:
    @functools.wraps(func)
    async def wrap(message) -> Callable:
        admins = await async_get_admin()
        if f"{message.from_user.id}" in admins:
            return await func(message)
    return wrap


async def update_users_list_async() -> None:
    """Update list of users for notification list in one thread mod"""
    async with REDIS_ASYNC_CONN as redis_connection:
        all_users = await Database().async_get_users()
        for user_id, data in all_users.items():
            await redis_connection.update_exist_key(user_id, data)
        await redis_connection.update_exist_key("users_list", all_users)


async def create_new_user(tg_id: int, username: str) -> bool:
    """Creating new user"""
    user_is_registered = await Database().create_user(tg_id=tg_id, name=username)
    if user_is_registered:
        await update_users_list_async()
        return user_is_registered
    return user_is_registered


async def async_get_admin() -> dict:
    """Update admin list for app in running"""
    async with REDIS_ASYNC_CONN as redis_connection:
        all_users = await redis_connection.get_value("users_list")
    only_admins = {admin: data for admin, data in all_users.items() if data["access"] == "ADMIN"}
    return only_admins


async def async_get_all_users() -> dict:
    """Update user list for admin panel if app has been running for a while"""
    async with REDIS_ASYNC_CONN as redis_connection:
        return await redis_connection.get_value("users_list")


async def delete_user_from_tg_id(user_tg_id: int) -> bool:
    """Deleting user by tg id"""
    is_deleted = await Database().delete_user(user_tg_id)
    if is_deleted:
        await update_users_list_async()
        return is_deleted
    return is_deleted


async def get_user_from_tg_id(user_tg_id: int) -> dict:
    """Receiving user by tg id"""
    async with REDIS_ASYNC_CONN as redis_connection:
        return await redis_connection.get_value(f"{user_tg_id}")


async def activate_notify(tg_id: int) -> bool:
    """Activation notifications on user"""
    is_activated = await Database().activate_notification(tg_id)
    if is_activated:
        await update_users_list_async()
        return is_activated
    return is_activated


async def deactivate_notify(tg_id: int) -> bool:
    """Deactivation notifications on user"""
    is_deactivated = await Database().deactivate_notification(tg_id)
    if is_deactivated:
        await update_users_list_async()
        return is_deactivated
    return is_deactivated


async def set_value_to_redis(value: str) -> bool:
    try:
        value = float(value)
    except ValueError:
        return False
    else:
        async with REDIS_ASYNC_CONN as session:
            await session.create_key_and_value("MINIMUM_VOLUME", value)
        return True

