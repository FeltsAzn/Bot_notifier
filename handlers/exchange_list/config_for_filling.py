from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.crud import Database
import math

page_counter = 1
elements_counter = 0
last_page = 1


async def filling_keyboard() -> InlineKeyboardMarkup:
    """Заполнение инлайн клавиатуры элементами базы данных"""
    global last_page

    last_page = math.ceil(len(users) / 6)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for tg_id, username, _ in users[elements_counter:6 + elements_counter]:
        button = InlineKeyboardButton(text=username, callback_data=f"{tg_id}:info:call")
        keyboard.insert(button)
    return keyboard


def add_of_value() -> None:
    """Повышение пагинации и изменение количества отображжаемых элементов"""
    global elements_counter
    global page_counter

    page_counter += 1
    elements_counter += 6


def diff_of_value() -> None:
    """Понижение пагинации и изменение количества отображжаемых элементов"""
    global elements_counter
    global page_counter

    elements_counter -= 6
    page_counter -= 1
