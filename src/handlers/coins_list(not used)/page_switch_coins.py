from aiogram.types import InlineKeyboardButton, CallbackQuery
from src.loader import dp
from src.handlers import filling_keyboard,\
    add_of_value, \
    diff_of_value, \
    last_page


page_counter = 1


@dp.callback_query_handler(text="next_page:coins:call")
async def next_pages_handler(call: CallbackQuery):
    """Прокрутка списка монет вперёд"""
    global page_counter

    state: bool = True if page_counter < last_page - 1 else False  # Проверка пагинации страницы для заполнения
    add_of_value()
    page_counter += 1
    keyboard = filling_keyboard()

    if state:
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:coins:call")
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:coins:call")
    else:
        left_button = InlineKeyboardButton(text="<<<<<<", callback_data="back_page:coins:call")
        right_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
    keyboard.insert(left_button)
    keyboard.insert(right_button)

    text = f"Список отслеживаемых монет ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="back_page:coins:call")
async def back_pages_handler(call: CallbackQuery):
    """Прокрутка списка монет назад"""
    global page_counter

    state: bool = True if page_counter > 2 else False  # Проверка пагинации страницы для заполнения
    diff_of_value()
    page_counter -= 1
    keyboard = filling_keyboard()

    if state:
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:coins:call")
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:coins:call")
    else:
        left_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        right_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:coins:call")
    keyboard.insert(left_button)
    keyboard.insert(right_button)

    text = f"Список отслеживаемых монет ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)
