from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from loader import dp
from aiogram.dispatcher.filters import Text
import math


places = [
    "Binance",
    "Kucoin",
    "Huobi",
    "Okx"
]
page_counter = 1
pages_sum = 0

@dp.message_handler(Text(equals="Список площадок"))
async def list_places(message: Message):
    keyboard = InlineKeyboardMarkup(row_width=2)

    for item in places[:5]:
        button = InlineKeyboardButton(text=item, callback_data=f"{item}:call")
        keyboard.insert(button)

    back_button = InlineKeyboardButton(text="<<< Назад", callback_data="back_page:call")
    next_button = InlineKeyboardButton(text="Далее >>>", callback_data="next_page:call")
    keyboard.insert(back_button)
    keyboard.insert(next_button)

    text = f"Список отслеживаемых площадок площадок ({page_counter})/{math.ceil(len(places)/5)}:"
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(text="next_page:call")
async def choose_service(call: CallbackQuery):
    global page_counter
    global pages_sum
    page_counter += 1

