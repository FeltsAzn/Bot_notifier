from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from utils.create_bot import dp, VolumeState
from handlers.admin_handler.config_for_filling import fill_table
from utils.middleware import admin_validator, set_value_to_redis
from aiogram.dispatcher import FSMContext

"""
Файл admin_panel.py - главный обработчик для доступа к админ-панели.
"""


@dp.message_handler(Text(equals="Admin panel"))
@admin_validator
async def start_admin_panel(message: Message):
    buttons = ['List of users', "Change minimal volume", "Admins settings", 'Back to user menu']
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


@dp.message_handler(Text(equals="Change minimal volume"))
@admin_validator
async def start(message: Message):
    buttons = ["Cancel set volume"]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer("Set minimum value of volume, which will boundary value", reply_markup=keyboard)
    await VolumeState.set_volume.set()


@dp.message_handler(state=VolumeState.set_volume)
async def set_volume(message: Message, state: FSMContext):
    if message.text == "Cancel set volume":
        await state.reset_state()
        return await start_admin_panel(message)

    is_right_volume = await set_value_to_redis(message.text)
    if is_right_volume:
        await state.reset_state()
        await message.answer(f"Boundary volume {message.text} set successfully")
        return await start_admin_panel(message)
    else:
        await message.answer(f"Value {message.text} is wrong, set right value")


