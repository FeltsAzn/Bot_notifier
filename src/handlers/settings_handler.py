import asyncio
from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp
from handlers.exception_handler import exception_hand
from middleware import (delete_user_from_tg_id,
                        activate_notify,
                        deactivate_notify,
                        validate_user,
                        get_user_from_tg_id)

"""
Файл settiongs_handler.py предназначен для реализации функционала бота "Settings" пользователя
основные кнопки "Выключение/включение уведомлений", "Удаление аккаунта" и "Домой". 
"""


@dp.message_handler(lambda mes: mes.text in ("Cancel deleting", "Settings"))
@validate_user
async def settings(message: types.Message, is_user: bool):
    if is_user:
        users = await get_user_from_tg_id(message.from_user.id)
        if users:
            match users["state"]:
                case "ACTIVATED":
                    buttons = ["Deactivate tracking", "Delete account", "Home"]
                case _:
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
async def stop_notify(message: types.Message, is_reg_user: bool):
    if is_reg_user:
        response: bool = await deactivate_notify(message.from_user.id)
        if response:
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
async def start_notify(message: types.Message, is_reg_user: bool):
    if is_reg_user:
        response: bool = await activate_notify(message.from_user.id)
        if response:
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
async def delete_user(message: types.Message, is_reg_user: bool):
    if is_reg_user:
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
async def deleting(message: types.Message, is_reg_user: bool):
    if is_reg_user:
        response = await delete_user_from_tg_id(message.from_user.id)
        if response:
            msg_id = await message.answer("Your account removed in database.\n"
                                          "If you want to get notifications \n"
                                          "about exchanges quotes again\n"
                                          "text /start for me", reply_markup=types.ReplyKeyboardRemove())
            await asyncio.sleep(5)
            await msg_id.delete()
        else:
            await exception_hand(message.from_user.id)
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()
