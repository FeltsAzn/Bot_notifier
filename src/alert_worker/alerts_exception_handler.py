import os
import aiogram
from aiogram import types

"""
Файл alerts_exception_handler.py - метод для отправки сообщения об ошибке
связанной с главным обработчиком уведомлений.  
"""

admin_url = os.getenv("ADMIN_NAME")

class UnexpectedException:
    def __init__(self, tg_id: int, bot_instance: aiogram.Bot):
        self.tg_id = tg_id
        self.bot = bot_instance

    async def exception_handler(self) -> None:
        start_buttons = ["Список площадок", "Настройки"]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*start_buttons)
        await self.bot.send_message(self.tg_id, "Возникла ошибка:(\n"
                                      f"Напишите администратору {admin_url}",
                               reply_markup=keyboard)