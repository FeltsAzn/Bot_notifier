import math
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


"""
Файл config_for_filling.py - методы для заполнения списка бирж и контроль
глобальных переменных для корректного переключения страничек 
"""


places = [
    "Binance",
    "Kucoin",
    "Huobi",
    "Okx",
    "Service1",
    "Service2",
    "Service3",
    "Service4",
    "Service5",
    "Service6",
    "Service7",
    "Service8",
    "Service9",
]

elements_counter = 0
last_page = math.ceil(len(places) / 6)


def filling_keyboard() -> InlineKeyboardMarkup:
    """Заполнение инлайн клавиатуры элементами базы данных"""
    global last_page

    keyboard = InlineKeyboardMarkup(row_width=2)
    for coin in places[elements_counter:6 + elements_counter]:
        button = InlineKeyboardButton(text=coin, callback_data=f"{coin}:exc:info:call")
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

