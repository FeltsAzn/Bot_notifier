from db.crud import Database
import multiprocessing
from alert_worker.alerts import update_user_cache


instance_cache = {}


def update_users_list_sync(instance: multiprocessing.Value = None) -> None:
    """Обновление списка пользователей для оповещений в мультипроцессорном режиме"""
    global instance_cache
    if instance is not None:
        instance.value = True
        instance_cache['state'] = instance
    else:
        instance = instance_cache['state']
        instance.value = True


async def update_users_list_async() -> None:
    """Обновление списка пользователей для оповещений в однопоточном асинхронном режиме"""
    await update_user_cache(True)


def sync_get_users_list() -> list:
    """Получение списка пользователей при старте приложения"""
    return Database().sync_get_users()


def sync_get_admin_list() -> list:
    """Получение списка админов при старте приложения"""
    response: list = Database().sync_get_users()
    only_admins = list(filter(lambda x: x[3] == "ADMIN", response))
    admin_list = list(map(lambda tup: tup[0], only_admins))
    return admin_list


async def create_new_user(tg_id: int, username: str) -> bool:
    """Создание нового пользователя"""
    return await Database().create_user(tg_id=tg_id, name=username)


async def async_update_admin_list() -> list:
    """Обновление списка списка админов """
    response: list = await Database().async_get_users()
    only_admins = list(filter(lambda x: x[3] == "ADMIN", response))
    admin_list = list(map(lambda tup: tup[0], only_admins))
    return admin_list


async def async_update_users_list() -> list[tuple]:
    """Обновление списка пользователей"""
    return await Database().async_get_users()
