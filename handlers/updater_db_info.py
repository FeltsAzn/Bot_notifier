from db.crud import Database


def sync_update_admin_list() -> list:
    response = Database().get_users_sync()
    only_admins = list(filter(lambda x: x[3] == "ADMIN", response))
    admin_list = list(map(lambda tup: tup[0], only_admins))
    return admin_list


async def async_update_admin_list() -> list:
    response = await Database().get_all_users()
    only_admins = list(filter(lambda x: x[3] == "ADMIN", response))
    admin_list = list(map(lambda tup: tup[0], only_admins))
    return admin_list
