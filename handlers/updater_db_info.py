from db.crud import Database


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
