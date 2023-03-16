import asyncio
from aiogram import types
from utils.create_bot import dp
from handlers.exception_handler import exception_hand
from utils.middleware import (async_get_admin,
                              create_new_user,
                              validate_user)

"""
Файл main_handler.py - стартовое меню бота. Осуществляет авторизацию, либо регистрацию пользователя.
"""


@dp.message_handler(commands=["start", "home"])
@validate_user
async def start(message: types.Message, is_reg_user: bool) -> None:
    """Start window"""
    buttons = ["List of places", "Settings"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    if is_reg_user:
        return await start_again(message)
    else:
        await new_user(message, keyboard, buttons)


async def new_user(message: types.Message,
                   keyboard: types.ReplyKeyboardMarkup,
                   buttons: list) -> None:
    """Handler for new user"""
    tg_id: int = message.from_user.id
    username: str = message.from_user.username if message.from_user.username else message.from_user.first_name
    is_user_created = await create_new_user(tg_id, username)
    if is_user_created:
        keyboard.add(*buttons)
        await message.answer("Hi, I am your assistant to tracking changes quotes!",
                             reply_markup=keyboard)
    else:
        await exception_hand(message.from_user.id)


@dp.message_handler(lambda mes: mes.text in ("Home", "Back to user menu"))
@validate_user
async def start_again(message: types.Message, is_reg_user: bool) -> None:
    if is_reg_user:
        admin_list = await async_get_admin()
        buttons = ["List of places", "Settings"]
        if f"{message.from_user.id}" in admin_list:
            buttons = ["List of places", "Admin panel", "Settings"]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*buttons)
        await message.answer("Back", reply_markup=keyboard)
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()
