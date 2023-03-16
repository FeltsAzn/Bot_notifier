from aiogram.types import InlineKeyboardButton, CallbackQuery
from handlers.exchange_list.config_for_filling import fill_kb
from utils.create_bot import dp


"""
Файл page_switch.py - обработчик переключений страничек для списка отслеживаемых бирж
"""


@dp.callback_query_handler(text="next_page:places:call")
async def next_pages_handler(call: CallbackQuery):
    """Прокрутка списка монет вперёд"""

    state: bool = True if fill_kb.page_counter < fill_kb.last_page - 1 else False  # Проверка пагинации страницы для заполнения
    fill_kb.up_values()
    keyboard = fill_kb.filling_keyboard()

    if state:
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:places:call")
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:places:call")

    else:
        left_button = InlineKeyboardButton(text="<<<<<<", callback_data="back_page:places:call")
        right_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
    keyboard.insert(left_button)
    keyboard.insert(right_button)

    text = f"List of tracking exchanges ({fill_kb.page_counter}/{fill_kb.last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="back_page:places:call")
async def back_pages_handler(call: CallbackQuery):
    """Прокрутка списка монет назад"""

    state = True if fill_kb.page_counter > 2 else False  # Проверка пагинации страницы для заполнения
    fill_kb.down_values()
    keyboard = fill_kb.filling_keyboard()

    if state:
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:places:call")
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:places:call")
    else:
        left_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        right_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:places:call")
    keyboard.insert(left_button)
    keyboard.insert(right_button)

    text = f"List of tracking exchanges ({fill_kb.page_counter}/{fill_kb.last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)
