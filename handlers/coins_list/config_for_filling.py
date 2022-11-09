from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import math

coins = [
    "BTC",
    "ETH",
    "TRX",
    "WAXL",
    "APT",
    "DOGE",
    "NEAR",
    "COIN1",
    "COIN2",
    "COIN3",
    "COIN4",
    "COIN5",
    "COIN6",
    "COIN7",
    "COIN8",
    "COIN9",
    "COIN10",
    "COIN11",
    "COIN12",
]


elements_counter = 0
last_page = math.ceil(len(coins) / 9)


def filling_keyboard() -> InlineKeyboardMarkup:
    """Заполнение инлайн клавиатуры элементами базы данных"""
    global last_page

    keyboard = InlineKeyboardMarkup(row_width=3)
    for coin in coins[elements_counter:9 + elements_counter]:
        button = InlineKeyboardButton(text=coin, callback_data=f"{coin}:coin:info:call")
        keyboard.insert(button)
    return keyboard


def add_of_value() -> None:
    """Повышение пагинации и изменение количества отображжаемых элементов"""
    global elements_counter

    elements_counter += 9



def diff_of_value() -> None:
    """Понижение пагинации и изменение количества отображжаемых элементов"""
    global elements_counter

    elements_counter -= 9
