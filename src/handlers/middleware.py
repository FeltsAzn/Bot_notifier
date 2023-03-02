import multiprocessing
from typing import Callable

from src.db.crud import Database
from src.alert_worker.alerts import update_user_cache, USER_CACHE


instance_cache = {}

"""
The middleware.py file is designed to hide database calls and filter data when a response is received.
from the database for readability of the code.
"""


def validate_user(func) -> Callable:
    user_cache = set(map(lambda x: x[0], USER_CACHE))

    def wrap(message) -> Callable:
        if message.from_user.id in user_cache:
            return func(message, True)
        return func(message, False)
    return wrap


def update_users_list_sync(instance: multiprocessing.Value = None) -> None:
    """Update list of users for notification list in multiprocess mod"""
    global instance_cache
    if instance is not None:
        instance.value = True
        instance_cache['state'] = instance
    else:
        instance = instance_cache['state']
        instance.value = True


async def update_users_list_async() -> None:
    """Update list of users for notification list in one thread mod"""
    await update_user_cache(True)


def sync_get_users_list() -> list:
    """Receiving list of users after app running"""
    return Database().sync_get_users()


def sync_get_admin_list() -> list:
    """Receiving list of admin after app running"""
    response: list = Database().sync_get_users()
    only_admins = list(filter(lambda x: x[3] == "ADMIN", response))
    admin_list = list(map(lambda tup: tup[0], only_admins))
    return admin_list


async def create_new_user(tg_id: int, username: str) -> bool:
    """Creating new user"""
    return await Database().create_user(tg_id=tg_id, name=username)


async def async_update_admin_list() -> list:
    """Update admin list for app in running"""
    response: list = await Database().async_get_users()
    only_admins = list(filter(lambda x: x[3] == "ADMIN", response))
    admin_list = list(map(lambda tup: tup[0], only_admins))
    return admin_list


async def async_update_users_list() -> list[tuple]:
    """Update user list for admin panel if app has been running for a while"""
    return await Database().async_get_users()


async def get_user_from_tg_id(user_tg_id: int) -> tuple | bool:
    """Receiving user by tg id"""
    return await Database().get_user(user_tg_id)


async def delete_user_from_tg_id(user_tg_id: int) -> bool:
    """Deleting user by tg id"""
    return await Database().delete_user(user_tg_id)


async def notify_activate() -> list[tuple] | bool:
    """List of all users with instance notifications"""
    return await Database().notifications_state()


async def activate_notify(tg_id: int) -> bool:
    """Activation notifications on user"""
    return await Database().active_notification(tg_id)


async def deactivate_notify(tg_id: int) -> bool:
    """Deactivation notifications on user"""
    return await Database().deactivated_notification(tg_id)

