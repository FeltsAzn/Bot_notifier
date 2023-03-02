from typing import Callable

from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from src.loader import dp
from src.handlers.admin_handler.config_for_filling import filling_keyboard, last_page
from src.handlers.middleware import async_update_admin_list, sync_get_admin_list

"""
Файл admin_panel.py - главный обработчик для доступа к админ-панели.
"""

admins: list = sync_get_admin_list()


def admin_validator(func) -> Callable:
    def wrap(message) -> Callable:
        if message.from_user.id in set(admins):
            return func(message)
    return wrap


@dp.message_handler(Text(equals="Admin panel"))
@admin_validator
async def start(message: Message):
    global admins

    admins = await async_update_admin_list()
    buttons = ['List of users', "Admins settings", 'Back to user menu']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Choose action:", reply_markup=keyboard)


@dp.message_handler(Text(equals="List of users"))
@admin_validator
async def start_list_of_users(message: Message):
    """Стартовый список пользователей"""
    global admins

    admins = await async_update_admin_list()
    keyboard = await filling_keyboard()
    if last_page > 1:
        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)
    text = f"List of users (1/{last_page}):"
    await message.answer(text, reply_markup=keyboard)


