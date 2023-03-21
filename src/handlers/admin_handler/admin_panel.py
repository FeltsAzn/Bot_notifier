from aiogram.types import Message, ReplyKeyboardMarkup
from utils.create_bot import dp
from utils.middleware import admin_validator

"""
Файл admin_panel.py - главный обработчик для доступа к админ-панели.
"""


@dp.message_handler(lambda message: message.text in {"Admin panel", "Back to admin panel"})
@admin_validator
async def start_admin_panel(message: Message):
    buttons = ["List of users", "Filter settings", "Admins settings", "Back to user menu"]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Choose action:", reply_markup=keyboard)
