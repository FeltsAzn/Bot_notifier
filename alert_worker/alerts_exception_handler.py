from aiogram import types
from dotenv import load_dotenv
import os

"""
Файл alerts_exception_handler.py - метод для отправки сообщения об ошибке
связанной с главным обработчиком уведомлений.  
"""

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
admin_url = os.getenv("ADMIN_NAME")


async def exception_handler(tg_id: int, bot) -> None:
    start_buttons = ['Список площадок', "Список валют", 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*start_buttons)
    await bot.send_message(tg_id, "Возникла ошибка:(\n"
                                  f"Напишите администратору {admin_url}",
                           reply_markup=keyboard)
