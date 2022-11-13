from aiogram import types
from loader import dp
from aiogram.dispatcher.filters import Text
from db.crud import Database
from handlers.updater_db_info import update_users_list_sync, update_users_list_async
from handlers.exception_handler import exception_hand

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
multiproc_config = os.getenv("MULTIPROCESSORING")


@dp.message_handler(lambda mes: mes.text in ("Отмена удаления", "Настройки"))
async def settings(message: types.Message):
    users = await Database().notifications_state()
    user_state = ''
    if users:
        for tg_id, state in users:
            if tg_id == message.from_user.id:
                user_state: str = state
        if user_state == "ACTIVATED":
            buttons = ["Приостановить отслеживание", 'Удалить аккаунт', 'Домой']
        else:
            buttons = ["Включить отслеживание", 'Удалить аккаунт', 'Домой']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*buttons)
        await message.answer("Выберите действия:", reply_markup=keyboard)
    else:
        await exception_hand(message.from_user.id)


@dp.message_handler(Text(equals="Приостановить отслеживание"))
async def stop_notify(message: types.Message):
    response = await Database().deactivated_notification(message.from_user.id)
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
    response = await Database().active_notification(message.from_user.id)
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


@dp.message_handler(Text(equals='Удалить аккаунт'))
async def delete_user(message: types.Message):
    buttons = ["Да, удалить аккаунт", 'Отмена удаления', 'Домой']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Вы действительно хотите\nудалить аккаунт?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Да, удалить аккаунт"))
async def deleting(message: types.Message):
    response = await Database().delete_user(message.from_user.id)
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



