from aiogram import types
from loader import dp


@dp.message_handler(commands=['start', 'home'])
async def start(message: types.Message):
    start_buttons = ['Список площадок', 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Привет, я твой помощник в отслеживании котировок",
                         reply_markup=keyboard)