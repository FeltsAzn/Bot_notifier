from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from utils.create_bot import dp
from handlers.admin_handler.config_for_filling import fill_table
from utils.middleware import admin_validator

"""
Файл admin_panel.py - главный обработчик для доступа к админ-панели.
"""


@dp.message_handler(Text(equals="Admin panel"))
@admin_validator
async def start_admin_panel(message: Message):
    buttons = ['List of users', "Filter settings", "Admins settings", 'Back to user menu']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Choose action:", reply_markup=keyboard)


@dp.message_handler(Text(equals="List of users"))
@admin_validator
async def start_list_of_users(message: Message):
    """Стартовый список пользователей"""
    keyboard = await fill_table.filling_keyboard()
    if fill_table.last_page > 1:
        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)
    text = f"List of users (1/{fill_table.last_page}):"
    await message.answer(text, reply_markup=keyboard)
