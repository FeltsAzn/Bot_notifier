from aiogram import types
from loader import dp
from keyboards.default.reply_keyboard import def_keyboard


@dp.message_handler(commands=['start', 'home'])
async def start(message: types.Message):
    start_buttons = ['Список площадок', 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*start_buttons)
    await message.answer("Привет, я твой помощник в отслеживании котировок",
                         reply_markup=keyboard)