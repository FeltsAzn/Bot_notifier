import math
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.middleware import get_all_users

"""
Файл config_for_filling.py - методы для заполнения административного списка пользователей и контроль
глобальных переменных для корректного переключения страничек 
"""


class FillingUserTable:

    def __init__(self):
        self.elements_counter = 0
        self.all_users = {}
        self.last_page = 0
        self.page_counter = 1

    async def update_user_list(self) -> None:
        """Получение списка всех пользователей"""
        self.all_users = await get_all_users()
        self.last_page = math.ceil(len(self.all_users) / 6)

    async def __call__(self) -> InlineKeyboardMarkup:
        """Заполнение инлайн клавиатуры элементами базы данных"""
        users = []
        await self.update_user_list()
        for tg_id, data in self.all_users.items():
            users.append((int(tg_id), data["username"]))
        keyboard = InlineKeyboardMarkup(row_width=2)

        for tg_id, username in users[self.elements_counter:6 + self.elements_counter]:
            button = InlineKeyboardButton(text=username, callback_data=f"{tg_id}:user:info:call")
            keyboard.insert(button)
        keyboard = self.insert_lower_button(keyboard)
        return keyboard

    def up_values(self) -> None:
        """Повышение пагинации и изменение количества отображжаемых элементов"""
        self.elements_counter += 6
        self.page_counter += 1

    def down_values(self) -> None:
        """Понижение пагинации и изменение количества отображжаемых элементов"""
        self.elements_counter -= 6
        self.page_counter -= 1

    def insert_lower_button(self, keyboard: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
        if self.page_counter == self.last_page and self.last_page != 1:
            right_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
            left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
            keyboard.add(left_button, right_button)

        elif self.page_counter > 1 and self.last_page != 2:
            right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
            left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
            keyboard.add(left_button, right_button)

        elif self.last_page > 1 and self.page_counter == 1:
            right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
            left_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
            keyboard.add(left_button, right_button)
        return keyboard

