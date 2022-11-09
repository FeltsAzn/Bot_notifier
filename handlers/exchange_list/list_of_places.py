from aiogram.types import Message, InlineKeyboardButton
from loader import dp
from aiogram.dispatcher.filters import Text
from handlers.exchange_list.config_for_filling import last_page, filling_keyboard


places = [
    "Binance",
    "Kucoin",
    "Huobi",
    "Okx",
    "Service1",
    "Service2",
    "Service3",
    "Service4",
    "Service5",
    "Service6",
    "Service7",
    "Service8",
    "Service9",
]


@dp.message_handler(Text(equals="Список площадок"))
async def list_of_places(message: Message):

    keyboard = filling_keyboard()
    if last_page > 1:
        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:places:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)

    text = f"Список отслеживаемых бирж (1/{last_page}):"
    await message.answer(text, reply_markup=keyboard)

