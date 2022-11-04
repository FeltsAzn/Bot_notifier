from aiogram import types
from loader import dp
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(equals="Список площадок"))
async def start(message: types.Message):
    buttons = ["<<< Назад", 'Далее >>>', 'Домой']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Список площадок:", reply_markup=keyboard)
