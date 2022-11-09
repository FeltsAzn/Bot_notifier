from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup
from loader import dp
from handlers.admin_handler.config_for_filling import filling_keyboard, last_page
from handlers.updater_db_info import async_update_admin_list, sync_update_admin_list

admins: list = sync_update_admin_list()


@dp.message_handler(lambda message: message.from_user.id in admins and message.text in ("Админка", "admin"))
async def start(message: Message):
    global admins

    admins = await async_update_admin_list()
    buttons = ['Список пользователей', "Настройки\nадминистритора", 'В меню пользователя']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.from_user.id in admins and message.text == "Список пользователей")
async def start_list_of_users(message: Message):
    """Стартовый список пользователей"""
    global admins

    admins = await async_update_admin_list()
    keyboard = await filling_keyboard()
    if last_page > 1:
        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)
    text = f"Список пользователей (1/{last_page}):"
    await message.answer(text, reply_markup=keyboard)


