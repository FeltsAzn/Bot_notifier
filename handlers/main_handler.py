from aiogram import types
from loader import dp
from handlers.updater_db_info import async_update_admin_list, create_new_user, async_update_users_list
from alert_worker.alerts import update_user_cache
from handlers.exception_handler import exteption_heand


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
    await update_user_cache()

    if data:
        keyboard.add(*buttons)
        await message.answer("Привет, я твой помощник в отслеживании котировок",
                             reply_markup=keyboard)
    else:
        await exteption_heand(message.from_user.id)


@dp.message_handler(lambda mes: mes.text in ("Домой", "В меню пользователя"))
async def start(message: types.Message) -> None:

    admin_list = await async_update_admin_list()
    buttons = ['Список площадок', 'Настройки']
    if message.from_user.id in admin_list:
        buttons = ['Список площадок', "Админка", 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Возвращаюсь домой", reply_markup=keyboard)
