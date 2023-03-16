from aiogram.types import InlineKeyboardButton, CallbackQuery
from utils.create_bot import dp
from handlers.admin_handler.config_for_filling import fill_table

"""
Файл page_switch.py - обработчик переключений страничек для административной панели пользователей
"""


@dp.callback_query_handler(text="next_page:user:call")
async def next_pages_handler(call: CallbackQuery):
    """Прокрутка списка пользователей вперёд"""
    state: bool = True if fill_table.page_counter < fill_table.last_page - 1 else False  # Проверка пагинации страницы для заполнения
    fill_table.up_values()
    keyboard = await fill_table.filling_keyboard()

    if state:
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
    else:
        left_button = InlineKeyboardButton(text="<<<<<<", callback_data="back_page:user:call")
        right_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
    keyboard.insert(left_button)
    keyboard.insert(right_button)

    text = f"List of users ({fill_table.page_counter}/{fill_table.last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="back_page:user:call")
async def back_pages_handler(call: CallbackQuery):
    """Прокрутка списка пользователей назад"""

    state: bool = True if fill_table.page_counter > 2 else False  # Проверка пагинации страницы для заполнения
    fill_table.down_values()
    keyboard = await fill_table.filling_keyboard()

    if state:
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
    else:
        left_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        right_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:user:call")
    keyboard.insert(left_button)
    keyboard.insert(right_button)

    text = f"List of users ({fill_table.page_counter}/{fill_table.last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)
