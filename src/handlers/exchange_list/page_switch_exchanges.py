from aiogram.types import InlineKeyboardButton, CallbackQuery
from loader import dp
from handlers.exchange_list.config_for_filling import (filling_keyboard,
                                                       add_of_value,
                                                       diff_of_value,
                                                       last_page
                                                       )

"""
Файл page_switch.py - обработчик переключений страничек для списка отслеживаемых бирж
"""

page_counter = 1


@dp.callback_query_handler(text="next_page:places:call")
async def next_pages_handler(call: CallbackQuery):
    """Прокрутка списка монет вперёд"""
    global page_counter

    state: bool = True if page_counter < last_page - 1 else False  # Проверка пагинации страницы для заполнения
    add_of_value()
    page_counter += 1
    keyboard = filling_keyboard()

    if state:
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:places:call")
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:places:call")

    else:
        left_button = InlineKeyboardButton(text="<<<<<<", callback_data="back_page:places:call")
        right_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
    keyboard.insert(left_button)
    keyboard.insert(right_button)

    text = f"List of tracking exchanges ({page_counter}/{last_page}):"
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
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:places:call")
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:places:call")
    else:
        left_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        right_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:places:call")
    keyboard.insert(left_button)
    keyboard.insert(right_button)

    text = f"List of tracking exchanges ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)
