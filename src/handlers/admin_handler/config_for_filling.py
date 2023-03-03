import math
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from middleware import sync_get_users_list, async_get_all_users


"""
Файл config_for_filling.py - методы для заполнения административного списка пользователей и контроль
глобальных переменных для корректного переключения страничек 
"""


elements_counter = 0

users_list: list = sync_get_users_list()
last_page = math.ceil(len(users_list) / 6)


async def get_user_list() -> list[tuple]:
    """Получение списка всех пользователей"""
    all_users = await async_get_all_users()
    list_of_users = []
    for user_id, data in all_users.items():
        list_of_users.append((user_id, data["username"]))
    return list_of_users


async def filling_keyboard() -> InlineKeyboardMarkup:
    """Заполнение инлайн клавиатуры элементами базы данных"""
    global last_page

    users: list[tuple] = await get_user_list()
    last_page = math.ceil(len(users) / 6)
    keyboard = InlineKeyboardMarkup(row_width=2)

    for tg_id, username in users[elements_counter:6 + elements_counter]:
        button = InlineKeyboardButton(text=username, callback_data=f"{tg_id}:user:info:call")
        keyboard.insert(button)
    return keyboard


def add_of_value() -> None:
    """Повышение пагинации и изменение количества отображжаемых элементов"""
    global elements_counter
    elements_counter += 6


def diff_of_value() -> None:
    """Понижение пагинации и изменение количества отображжаемых элементов"""
    global elements_counter

    elements_counter -= 6
