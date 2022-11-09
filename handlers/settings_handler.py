from aiogram import types
from loader import dp
from aiogram.dispatcher.filters import Text
from db.crud import Database
from alert_worker.alerts import update_user_cache
from handlers.exception_handler import exteption_heand


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
        await exteption_heand(message.from_user.id)


@dp.message_handler(Text(equals="Приостановить отслеживание"))
async def stop_notify(message: types.Message):
    response = await Database().deactivated_notification(message.from_user.id)
    if response:
        await update_user_cache()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add("Домой")
        await message.answer("Отслеживание деактивировано", reply_markup=keyboard)
    else:
        await exteption_heand(message.from_user.id)


@dp.message_handler(Text(equals="Включить отслеживание"))
async def start_notify(message: types.Message):
    response = await Database().active_notification(message.from_user.id)
    if response:
        await update_user_cache()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add("Домой")
        await message.answer("Отслеживание активировано", reply_markup=keyboard)
    else:
        await exteption_heand(message.from_user.id)


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
        await update_user_cache()
        await message.answer("Ваш аккаунт удален из базы.\n"
                             "Чтобы снова попасть в базу бота\n"
                             "для получения уведомлений о состоянии биржи\n"
                             "наберите /start")
    else:
        await exteption_heand(message.from_user.id)



