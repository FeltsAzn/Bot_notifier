from aiogram import types
from loader import dp
from handlers.exception_handler import exception_hand
from handlers.middleware import async_update_admin_list,\
    create_new_user, \
    async_update_users_list, \
    update_users_list_sync, \
    update_users_list_async
import os

"""
Файл main_handler.py - стартовое меню бота. Осуществляет авторизацию, либо регистрацию пользователя.
"""


multiproc_config = os.getenv("MULTIPROCESSORING")


@dp.message_handler(commands=['start', 'home'])
async def start(message: types.Message) -> None:
    """Стартовое окно"""

    admin_list = await async_update_admin_list()
    all_users = list(map(lambda user: user[0], await async_update_users_list()))

    buttons = ['Список площадок', 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    if all_users and message.from_user.id in all_users:
        await user_in_users_list(admin_list, message, keyboard, buttons)

    else:
        await new_user(message, keyboard, buttons)


async def user_in_users_list(admins: list,
                             message: types.Message,
                             keyboard: types.ReplyKeyboardMarkup,
                             buttons: list) -> None:
    """Обработчик существующиего пользователя"""
    if message.from_user.id in admins:
        buttons = ['Список площадок', "Админка", 'Настройки']
    keyboard.add(*buttons)
    await message.answer("Привет, я твой помощник в отслеживании котировок",
                         reply_markup=keyboard)


async def new_user(message: types.Message,
                   keyboard: types.ReplyKeyboardMarkup,
                   buttons: list) -> None:
    """Обработчик нового пользователя"""
    tg_id: int = message.from_user.id
    username: str = message.from_user.username if message.from_user.username else message.from_user.first_name
    data = await create_new_user(tg_id, username)
    if multiproc_config.upper() == "ON":
        update_users_list_sync()
    else:
        await update_users_list_async()

    if data:
        keyboard.add(*buttons)
        await message.answer("Привет, я твой помощник в отслеживании котировок",
                             reply_markup=keyboard)
    else:
        await exception_hand(message.from_user.id)


@dp.message_handler(lambda mes: mes.text in ("Домой", "В меню пользователя"))
async def start(message: types.Message) -> None:

    admin_list = await async_update_admin_list()
    buttons = ['Список площадок', 'Настройки']
    if message.from_user.id in admin_list:
        buttons = ['Список площадок', "Админка", 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Возвращаюсь домой", reply_markup=keyboard)
