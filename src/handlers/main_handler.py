import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.create_bot import dp, bot
from handlers.exception_handler import exception_hand
from utils.virtual_variables import MAIN_ADMIN
from utils.middleware import (get_admins,
                              create_new_user,
                              validate_user)

"""
Файл main_handler.py - стартовое меню бота. Осуществляет авторизацию, либо регистрацию пользователя.
"""


@dp.message_handler(commands=["start", "home"])
@validate_user
async def start(message: types.Message, is_reg_user: bool, state: FSMContext) -> None:
    """Start window"""
    if state:
        await state.reset_state()
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
        await bot.send_message(chat_id=MAIN_ADMIN, text=f"User @{username} registered on bot.")
    else:
        await bot.send_message(chat_id=MAIN_ADMIN, text=f"User @{username} try to register to bot.")
        await exception_hand(message.from_user.id)


@dp.message_handler(lambda mes: mes.text in {"Home", "Back to user menu"})
@validate_user
async def start_again(message: types.Message, is_reg_user: bool, state: FSMContext) -> None:
    if is_reg_user:
        if state:
            await state.reset_state()
        admin_list = await get_admins()
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
