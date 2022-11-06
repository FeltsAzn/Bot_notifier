from aiogram import types
from loader import dp
from db.crud import Database


@dp.message_handler(commands=['start', 'home'])
async def start(message: types.Message):
    start_buttons = ['Список площадок', 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    data = await Database().create_user(tg_id=message.from_user.id,
                                        name=message.from_user.username)
    if data:
        keyboard.add(*start_buttons)
        await message.answer("Привет, я твой помощник в отслеживании котировок",
                             reply_markup=keyboard)
    else:
        await message.answer("Возникла ошибка:(\n"
                             "Напишите администратору https://t.me/5703780641",
                             reply_markup=keyboard)