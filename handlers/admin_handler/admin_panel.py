from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
import os
from loader import dp
from handlers.admin_handler.config_for_filling import filling_keyboard, last_page, page_counter


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
admin_id = list(map(lambda tg_id: int(tg_id), os.getenv("ADMIN_ID").split(',')))


@dp.message_handler(lambda message: message.from_user.id in admin_id and message.text in ("Админка", "admin"))
async def start(message: Message):
    buttons = ['Список пользователей', "Настройки\nадминистритора", 'В меню пользователя']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.from_user.id in admin_id and message.text == "Список пользователей")
async def start_list_of_users(message: Message):
    """Стартовый список пользователей"""

    keyboard = await filling_keyboard()
    if last_page > 1:
        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)
    text = f"Список пользователей ({page_counter}/{last_page}):"
    await message.answer(text, reply_markup=keyboard)


