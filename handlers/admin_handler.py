from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv
import math
import os
from loader import dp
from db.crud import Database


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
admin_id = os.getenv("ADMIN_ID")


page_counter = 1
elements_counter = 0
last_page = 1


async def get_user_list() -> list[tuple]:
    """Получение списка всех пользователей"""
    users = await Database().get_all_users()
    return users


@dp.message_handler(lambda message: message.from_user.id == int(admin_id),
                    commands=["admin"])
async def list_of_users(message: Message):
    global page_counter
    global elements_counter
    global last_page

    users = await get_user_list()
    page_counter = 1
    elements_counter = 0
    last_page = math.ceil(len(users) / 6)

    keyboard = InlineKeyboardMarkup(row_width=2)

    for tg_id, username, _ in users[:6]:
        button = InlineKeyboardButton(text=username, callback_data=f"{tg_id}:info:call")
        keyboard.insert(button)

    next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:user:call")
    stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
    keyboard.insert(stop_button)
    keyboard.insert(next_button)

    text = f"Список пользователей ({page_counter}/{last_page}):"
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(text_contains=":info:call")
async def user_info(call: CallbackQuery):
    """получение информации по конкретному пользователю"""
    print(call.message.text)
    tg_id, username, state = await Database().get_user(call.from_user.id)

    await call.message.answer(text=f'<i>tg_id</i>: <b>{tg_id}</b>\n'
                                   f'<i>name</i>: <b>{username}</b>\n'
                                   f'<i>notify</i>: <b>{state}</b>',
                              parse_mode='html')


@dp.callback_query_handler(text="next_page:user:call")
async def next_pages_handler(call: CallbackQuery):
    global page_counter
    global elements_counter

    if page_counter < last_page - 1:
        add_of_var()
        keyboard = await filling_keyboard()

        back_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        keyboard.insert(back_button)
        keyboard.insert(next_button)
    else:
        add_of_var()
        keyboard = await filling_keyboard()

        back_button = InlineKeyboardButton(text="<<<<<<", callback_data="back_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(back_button)
        keyboard.insert(stop_button)

    text = f"Список пользователей ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="back_page:user:call")
async def back_pages_handler(call: CallbackQuery):
    global page_counter
    global elements_counter

    if page_counter > 2:
        diff_of_var()
        keyboard = await filling_keyboard()

        back_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        keyboard.insert(back_button)
        keyboard.insert(next_button)
    else:
        diff_of_var()
        keyboard = await filling_keyboard()

        next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)

    text = f"Список пользователей ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


async def filling_keyboard():
    users = await get_user_list()
    keyboard = InlineKeyboardMarkup(row_width=2)
    for tg_id, username, _ in users[elements_counter:6 + elements_counter]:
        button = InlineKeyboardButton(text=username, callback_data=f"{tg_id}:info:call")
        keyboard.insert(button)
    return keyboard


def add_of_var():
    global elements_counter
    global page_counter

    page_counter += 1
    elements_counter += 6


def diff_of_var():
    global elements_counter
    global page_counter

    elements_counter -= 6
    page_counter -= 1
