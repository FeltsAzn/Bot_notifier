from aiogram.types import InlineKeyboardButton, CallbackQuery
from loader import dp
from handlers.exchange_list.config_for_filling import filling_keyboard,\
    add_of_value, \
    diff_of_value, \
    last_page

page_counter = 1


@dp.callback_query_handler(text="next_page:places:call")
async def next_pages_handler(call: CallbackQuery):
    """Прокрутка списка монет вперёд"""
    global page_counter

    state = True if page_counter < last_page - 1 else False  # Проверка пагинации страницы для заполнения
    add_of_value()
    page_counter += 1
    keyboard = filling_keyboard()

    if state:
        back_button = InlineKeyboardButton(text="<<<", callback_data="back_page:places:call")
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:places:call")
        keyboard.insert(back_button)
        keyboard.insert(next_button)
    else:
        back_button = InlineKeyboardButton(text="<<<<<<", callback_data="back_page:places:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(back_button)
        keyboard.insert(stop_button)

    text = f"Список отслеживаемых бирж ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="back_page:places:call")
async def back_pages_handler(call: CallbackQuery):
    """Прокрутка списка монет назад"""
    global page_counter

    state = True if page_counter > 2 else False  # Проверка пагинации страницы для заполнения
    diff_of_value()
    page_counter -= 1
    keyboard = filling_keyboard()

    if state:
        back_button = InlineKeyboardButton(text="<<<", callback_data="back_page:places:call")
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:places:call")
        keyboard.insert(back_button)
        keyboard.insert(next_button)
    else:
        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:places:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)

    text = f"Список отслеживаемых бирж ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)

