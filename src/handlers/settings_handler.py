import asyncio
import os
from aiogram import types
from aiogram.dispatcher.filters import Text
from src.loader import dp
from src.handlers.exception_handler import exception_hand
from src.handlers.middleware import (update_users_list_sync,
                                     update_users_list_async,
                                     delete_user_from_tg_id,
                                     notify_activate,
                                     activate_notify,
                                     deactivate_notify,
                                     validate_user)

"""
Файл settiongs_handler.py предназначен для реализации функционала бота "Settings" пользователя
основные кнопки "Выключение/включение уведомлений", "Удаление аккаунта" и "Домой". 
"""

multiproc_config = os.getenv("MULTIPROCESSORING")


@dp.message_handler(lambda mes: mes.text in ("Cancel deleting", "Settings"))
@validate_user
async def settings(message: types.Message, is_user: bool):
    if is_user:
        users = await notify_activate()
        user_state = ''
        if users:
            for tg_id, state in users:
                if tg_id == message.from_user.id:
                    user_state: str = state
            if user_state == "ACTIVATED":
                buttons = ["Deactivate tracking", "Delete account", "Home"]
            else:
                buttons = ["Activate tracking", "Delete account", "Home"]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            keyboard.add(*buttons)
            await message.answer("Choose action:", reply_markup=keyboard)
        else:
            await exception_hand(message.from_user.id)
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()


@dp.message_handler(Text(equals="Deactivate tracking"))
@validate_user
async def stop_notify(message: types.Message, is_user: bool):
    if is_user:
        response: bool = await deactivate_notify(message.from_user.id)
        if response:
            if multiproc_config.upper() == "ON":
                update_users_list_sync()
            else:
                await update_users_list_async()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            keyboard.add("Home")
            await message.answer("Tracking deactivated", reply_markup=keyboard)
        else:
            await exception_hand(message.from_user.id)
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()


@dp.message_handler(Text(equals="Activate tracking"))
@validate_user
async def start_notify(message: types.Message, is_user: bool):
    if is_user:
        response: bool = await activate_notify(message.from_user.id)
        if response:
            if multiproc_config.upper() == "ON":
                update_users_list_sync()
            else:
                await update_users_list_async()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            keyboard.add("Home")
            await message.answer("Tracking activated", reply_markup=keyboard)
        else:
            await exception_hand(message.from_user.id)
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()


@dp.message_handler(Text(equals="Delete account"))
@validate_user
async def delete_user(message: types.Message, is_user: bool):
    if is_user:
        buttons = ["Yes, delete my account", "Cancel deleting", "Home"]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*buttons)
        await message.answer("Are you sure\nto delete account?", reply_markup=keyboard)
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()


@dp.message_handler(Text(equals="Yes, delete my account"))
@validate_user
async def deleting(message: types.Message, is_user: bool):
    if is_user:
        response = await delete_user_from_tg_id(message.from_user.id)
        if response:
            if multiproc_config.upper() == "ON":
                update_users_list_sync()
            else:
                await update_users_list_async()
            await message.answer("Your account removed in database.\n"
                                 "If you want to get notifications \n"
                                 "about exchanges quotes again\n"
                                 "text /start for me")
        else:
            await exception_hand(message.from_user.id)
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()
