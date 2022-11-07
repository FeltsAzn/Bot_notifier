from aiogram import types
from loader import dp
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(equals="Настройки"))
async def settings(message: types.Message):
    buttons = ["Добавить новую площадку", 'Удалить площадку', 'Домой']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Выберите действия:", reply_markup=keyboard)

