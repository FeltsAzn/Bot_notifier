from aiogram.types import Message, InlineKeyboardButton
from loader import dp
from aiogram.dispatcher.filters import Text
from handlers.coins_list.config_for_filling import last_page, filling_keyboard


@dp.message_handler(Text(equals="Список валют"))
async def list_of_coins(message: Message):
    """Начальное заполнение списка монет"""
    keyboard = filling_keyboard()

    if last_page > 1:
        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:coins:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)

    text = f"Список отслеживаемых монет (1/{last_page}):"
    await message.answer(text, reply_markup=keyboard)




