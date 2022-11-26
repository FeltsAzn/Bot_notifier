import os
from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp
from handlers.exception_handler import exception_hand
from handlers.middleware import update_users_list_sync, update_users_list_async, delete_user_from_tg_id, \
    notify_activate, activate_notify, deactivate_notify


"""
Файл settiongs_handler.py предназначен для реализации функционала бота "настройки" пользователя
основные кнопки "Выключение/включение уведомлений", "Удаление аккаунта" и "Домой". 
"""

multiproc_config = os.getenv("MULTIPROCESSORING")


@dp.message_handler(lambda mes: mes.text in ("Отмена удаления", "Настройки"))
async def settings(message: types.Message):
    users = await notify_activate()
    user_state = ''
    if users:
        for tg_id, state in users:
            if tg_id == message.from_user.id:
                user_state: str = state
        if user_state == "ACTIVATED":
            buttons = ["Приостановить отслеживание", "Удалить аккаунт", "Домой"]
        else:
            buttons = ["Включить отслеживание", "Удалить аккаунт", "Домой"]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*buttons)
        await message.answer("Выберите действия:", reply_markup=keyboard)
    else:
        await exception_hand(message.from_user.id)


@dp.message_handler(Text(equals="Приостановить отслеживание"))
async def stop_notify(message: types.Message):
    response: bool = await deactivate_notify(message.from_user.id)
    if response:
        if multiproc_config.upper() == "ON":
            update_users_list_sync()
        else:
            await update_users_list_async()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add("Домой")
        await message.answer("Отслеживание деактивировано", reply_markup=keyboard)
    else:
        await exception_hand(message.from_user.id)


@dp.message_handler(Text(equals="Включить отслеживание"))
async def start_notify(message: types.Message):
    response: bool = await activate_notify(message.from_user.id)
    if response:
        if multiproc_config.upper() == "ON":
            update_users_list_sync()
        else:
            await update_users_list_async()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add("Домой")
        await message.answer("Отслеживание активировано", reply_markup=keyboard)
    else:
        await exception_hand(message.from_user.id)


@dp.message_handler(Text(equals="Удалить аккаунт"))
async def delete_user(message: types.Message):
    buttons = ["Да, удалить аккаунт", "Отмена удаления", "Домой"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Вы действительно хотите\nудалить аккаунт?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Да, удалить аккаунт"))
async def deleting(message: types.Message):
    response = await delete_user_from_tg_id(message.from_user.id)
    if response:
        if multiproc_config.upper() == "ON":
            update_users_list_sync()
        else:
            await update_users_list_async()
        await message.answer("Ваш аккаунт удален из базы.\n"
                             "Чтобы снова попасть в базу бота\n"
                             "для получения уведомлений о состоянии биржи\n"
                             "наберите /start")
    else:
        await exception_hand(message.from_user.id)
