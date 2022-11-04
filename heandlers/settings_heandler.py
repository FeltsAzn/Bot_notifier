from aiogram import types
from loader import dp
from aiogram.dispatcher.filters import Text
from keyboards.default.reply_keyboard import def_keyboard


@dp.message_handler(Text(equals="Настройки"))
async def start(message: types.Message):
    buttons = ["Добавить новую площадку", 'Удалить площадку', 'Домой']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Выберите действия:", reply_markup=keyboard)
    await message.answer(text=message.chat.id)
