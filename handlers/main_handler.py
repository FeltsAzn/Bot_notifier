from aiogram import types
from loader import dp
from db.crud import Database
from handlers.updater_db_info import sync_update_admin_list, async_update_admin_list
from alert_worker.alerts import update_user_cache
from handlers.exception_handler import exteption_heand

admin_list: list = sync_update_admin_list()


@dp.message_handler(commands=['start', 'home'])
async def start(message: types.Message):
    """Стартовое окно"""
    global admin_list

    admin_list = await async_update_admin_list()
    start_buttons = ['Список площадок', "Список валют", 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    all_users = await Database().get_all_users()

    if message.from_user.id in admin_list:
        start_buttons = ['Список площадок', "Список валют", "Админка", 'Настройки']
    if all_users and message.from_user.id in all_users:
        keyboard.add(*start_buttons)

        await message.answer("Привет, я твой помощник в отслеживании котировок",
                             reply_markup=keyboard)
    else:
        tg_id = message.from_user.id
        username = message.from_user.username
        data = await Database().create_user(tg_id=tg_id,
                                            name=username if username else message.from_user.first_name)
        await update_user_cache()
        if data:
            keyboard.add(*start_buttons)
            await message.answer("Привет, я твой помощник в отслеживании котировок",
                                 reply_markup=keyboard)

        else:
            await exteption_heand(message.from_user.id)


@dp.message_handler(lambda mes: mes.text in ("Домой", "В меню пользователя"))
async def start(message: types.Message):
    global admin_list

    admin_list = await async_update_admin_list()
    buttons = ['Список площадок', "Список валют", 'Настройки']
    if message.from_user.id in admin_list:
        buttons = ['Список площадок', "Список валют", "Админка", 'Настройки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Возвращаюсь домой", reply_markup=keyboard)
