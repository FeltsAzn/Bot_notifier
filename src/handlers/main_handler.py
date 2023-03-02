import asyncio
import os
from aiogram import types
from src.loader import dp
from src.handlers.exception_handler import exception_hand
from src.handlers.middleware import (async_update_admin_list,
                                     create_new_user,
                                     async_update_users_list,
                                     update_users_list_sync,
                                     update_users_list_async,
                                     validate_user)

"""
Файл main_handler.py - стартовое меню бота. Осуществляет авторизацию, либо регистрацию пользователя.
"""

multiproc_config = os.getenv("MULTIPROCESSORING")


@dp.message_handler(commands=["start", "home"])
async def start(message: types.Message) -> None:
    """Start window"""
    admin_list = await async_update_admin_list()
    all_users = list(map(lambda user: user[0], await async_update_users_list()))

    buttons = ["List of places", "Settings"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    if all_users and message.from_user.id in all_users:
        await user_in_users_list(admin_list, message, keyboard, buttons)

    else:
        await new_user(message, keyboard, buttons)


async def user_in_users_list(admins: list,
                             message: types.Message,
                             keyboard: types.ReplyKeyboardMarkup,
                             buttons: list) -> None:
    """Handler for existed user"""
    if message.from_user.id in admins:
        buttons = ["List of places", "Admin Panel", "Settings"]
    keyboard.add(*buttons)
    await message.answer("Hi, I am your assistant to tracking changes quotes!",
                         reply_markup=keyboard)


async def new_user(message: types.Message,
                   keyboard: types.ReplyKeyboardMarkup,
                   buttons: list) -> None:
    """Handler for new user"""
    tg_id: int = message.from_user.id
    username: str = message.from_user.username if message.from_user.username else message.from_user.first_name
    data = await create_new_user(tg_id, username)
    if multiproc_config.upper() == "ON":
        update_users_list_sync()
    else:
        await update_users_list_async()

    if data:
        keyboard.add(*buttons)
        await message.answer("Hi, I am your assistant to tracking changes quotes!",
                             reply_markup=keyboard)
    else:
        await exception_hand(message.from_user.id)


@dp.message_handler(lambda mes: mes.text in ("Home", "Back to user menu"))
@validate_user
async def start_again(message: types.Message, is_user) -> None:
    if is_user:
        admin_list = await async_update_admin_list()
        buttons = ["List of places", "Settings"]
        if message.from_user.id in admin_list:
            buttons = ["List of places", "Admin panel", "Settings"]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*buttons)
        msg_id = await message.answer("Back", reply_markup=keyboard)
        await asyncio.sleep(2)
        await msg_id.delete()
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()
