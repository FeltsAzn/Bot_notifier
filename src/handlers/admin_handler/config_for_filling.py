import math
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from middleware import async_get_all_users

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
        self.all_users = await async_get_all_users()
        self.last_page = math.ceil(len(self.all_users) / 6)

    async def filling_keyboard(self) -> InlineKeyboardMarkup:
        """Заполнение инлайн клавиатуры элементами базы данных"""
        users = []
        await self.update_user_list()
        for tg_id, data in self.all_users.items():
            users.append((int(tg_id), data["username"]))
        keyboard = InlineKeyboardMarkup(row_width=2)

        for tg_id, username in users[self.elements_counter:6 + self.elements_counter]:
            button = InlineKeyboardButton(text=username, callback_data=f"{tg_id}:user:info:call")
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


fill_table = FillingUserTable()
