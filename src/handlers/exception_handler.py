import os
from aiogram import types
from src.loader import bot


"""
Файл exception_handler.py - при возникновении ошибки в меню управления (удаление или получение информации)
присылает пользователям уведомление об ошибке.
"""


admin_url = os.getenv("ADMIN_NAME")


async def exception_hand(tg_id: int) -> None:
    start_buttons = ["List of places", "List of currencies", "Home"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*start_buttons)
    await bot.send_message(tg_id, "Error :(\n"
                                  f"Text to administrator: {admin_url}",
                           reply_markup=keyboard)
