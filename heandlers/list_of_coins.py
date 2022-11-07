from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from loader import dp
from aiogram.dispatcher.filters import Text
import math

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
page_counter = 1
elements_counter = 0
last_page = math.ceil(len(places) / 6)


@dp.message_handler(Text(equals="Список валют"))
async def list_places(message: Message):
    global page_counter
    global elements_counter
    page_counter = 1
    elements_counter = 0

    keyboard = InlineKeyboardMarkup(row_width=2)

    for item in places[:6]:
        button = InlineKeyboardButton(text=item, callback_data=f"{item}:call")
        keyboard.insert(button)

    next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:call")
    stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
    keyboard.insert(stop_button)
    keyboard.insert(next_button)

    text = f"Список отслеживаемых площадок площадок ({page_counter}/{last_page}):"
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(text="next_page:call")
async def next_pages_heandler(call: CallbackQuery):
    global page_counter
    global elements_counter

    elements_counter += 6
    page_counter += 1
    keyboard = InlineKeyboardMarkup(row_width=2)

    for item in places[elements_counter:6 + elements_counter]:
        button = InlineKeyboardButton(text=item, callback_data=f"{item}:call")
        keyboard.insert(button)

    if page_counter < last_page - 1:
        back_button = InlineKeyboardButton(text="<<<", callback_data="back_page:call")
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:call")
        keyboard.insert(back_button)
        keyboard.insert(next_button)
    else:
        back_button = InlineKeyboardButton(text="<<<<<<", callback_data="back_page:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(back_button)
        keyboard.insert(stop_button)

    text = f"Список отслеживаемых площадок площадок ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="back_page:call")
async def back_pages_heandler(call: CallbackQuery):
    global page_counter
    global elements_counter

    elements_counter -= 6
    page_counter -= 1
    keyboard = InlineKeyboardMarkup(row_width=2)

    for item in places[elements_counter:6 + elements_counter]:
        button = InlineKeyboardButton(text=item, callback_data=f"{item}:call")
        keyboard.insert(button)

    if page_counter > 2:
        back_button = InlineKeyboardButton(text="<<<", callback_data="back_page:call")
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:call")
        keyboard.insert(back_button)
        keyboard.insert(next_button)
    else:
        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)

    text = f"Список отслеживаемых площадок площадок ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)
