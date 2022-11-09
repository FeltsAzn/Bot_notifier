from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.crud import Database
import math


elements_counter = 0
users: list = Database().get_users_sync()
last_page = math.ceil(len(users) / 6)


async def get_user_list() -> list[tuple]:
    """Получение списка всех пользователей"""
    users = await Database().get_all_users()
    return users


async def filling_keyboard() -> InlineKeyboardMarkup:
    """Заполнение инлайн клавиатуры элементами базы данных"""
    global last_page

    users = await get_user_list()
    last_page = math.ceil(len(users) / 6)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for tg_id, username, _, _ in users[elements_counter:6 + elements_counter]:
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
