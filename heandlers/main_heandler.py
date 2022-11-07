from aiogram import types
from loader import dp
from db.crud import Database
from aiogram.dispatcher.filters import Text
from alert_worker.alerts import update_user_cache


@dp.message_handler(commands=['start', 'home'])
async def start(message: types.Message):
    start_buttons = ['Список площадок', "Список валют", 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if message.from_user.id in await Database().get_users():
        keyboard.add(*start_buttons)

        await message.answer("Привет, я твой помощник в отслеживании котировок",
                             reply_markup=keyboard)
    else:
        data = await Database().create_user(tg_id=message.from_user.id,
                                            name=message.from_user.username)
        await update_user_cache()
        if data:
            keyboard.add(*start_buttons)
            await message.answer("Привет, я твой помощник в отслеживании котировок",
                                 reply_markup=keyboard)

        else:
            await message.answer("Возникла ошибка:(\n"
                                 "Напишите администратору https://t.me/5703780641",
                                 reply_markup=keyboard)


@dp.message_handler(Text(equals="Домой"))
async def start(message: types.Message):
    buttons = ['Список площадок', "Список валют", 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Возвращаюсь домой", reply_markup=keyboard)
