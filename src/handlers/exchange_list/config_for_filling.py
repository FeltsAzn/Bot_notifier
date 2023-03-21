import math
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""
Файл config_for_filling.py - методы для заполнения списка бирж и контроль
глобальных переменных для корректного переключения страничек 
"""

# TODO: Add state for correct work filling keyboard


class FillingKeyboard:
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

    def __init__(self):
        self.elements_counter = 0
        self.page_counter = 1
        self.last_page = math.ceil(len(self.places) / 6)

    def fill_keyboard(self) -> InlineKeyboardMarkup:
        """Заполнение инлайн клавиатуры элементами базы данных"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        for coin in self.places[self.elements_counter:6 + self.elements_counter]:
            button = InlineKeyboardButton(text=coin, callback_data=f"{coin}:exc:info:call")
            keyboard.insert(button)
        return keyboard

    def up_values(self) -> None:
        """Повышение пагинации и изменение количества отображжаемых элементов"""
        self.elements_counter += 6
        self.page_counter += 1

    def down_values(self) -> None:
        """Понижение пагинации и изменение количества отображжаемых элементов"""
        self.elements_counter -= 6
        self.page_counter -= 1


fill_kb = FillingKeyboard()
