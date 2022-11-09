from aiogram.types import InlineKeyboardButton, CallbackQuery
from loader import dp
from handlers.exchange_list.config_for_filling import filling_keyboard,\
    add_of_value, \
    diff_of_value, \
    page_counter, \
    last_page


@dp.callback_query_handler(text="next_page:user:call")
async def next_pages_handler(call: CallbackQuery):
    """Прокрутка списка пользователей вперёд"""

    state = True if page_counter < last_page - 1 else False  # Проверка пагинации страницы для заполнения
    add_of_value()
    keyboard = await filling_keyboard()
    if state:
        back_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        keyboard.insert(back_button)
        keyboard.insert(next_button)
    else:
        back_button = InlineKeyboardButton(text="<<<<<<", callback_data="back_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(back_button)
        keyboard.insert(stop_button)

    text = f"Список пользователей ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="back_page:user:call")
async def back_pages_handler(call: CallbackQuery):
    """Прокрутка списка пользователей назад"""

    state = True if page_counter > 2 else False  # Проверка пагинации страницы для заполнения
    diff_of_value()
    keyboard = await filling_keyboard()

    if state:
        back_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        keyboard.insert(back_button)
        keyboard.insert(next_button)
    else:
        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)

    text = f"Список пользователей ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)
