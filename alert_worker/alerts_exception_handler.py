import os
from aiogram import types

"""
Файл alerts_exception_handler.py - метод для отправки сообщения об ошибке
связанной с главным обработчиком уведомлений.  
"""

admin_url = os.getenv("ADMIN_NAME")


async def exception_handler(tg_id: int, bot) -> None:
    start_buttons = ["Список площадок", "Настройки"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*start_buttons)
    await bot.send_message(tg_id, "Возникла ошибка:(\n"
                                  f"Напишите администратору {admin_url}",
                           reply_markup=keyboard)
