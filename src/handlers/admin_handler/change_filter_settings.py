from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, CallbackQuery
from aiogram.dispatcher.filters import Text
from utils.create_bot import dp, VolumeState
from utils.middleware import admin_validator, set_value_to_redis, get_settings
from aiogram.dispatcher import FSMContext


@dp.message_handler(Text(equals="Filter settings"))
@admin_validator
async def show_settings(message: Message):
    settings = await get_settings()
    volume = InlineKeyboardButton(text=f"Volume: {settings['volume']}$",
                                  callback_data="volume:change:call")
    start_percent = InlineKeyboardButton(text=f"Start: {settings['start']}%",
                                         callback_data="start:change:call")
    up_percent = InlineKeyboardButton(text=f"Up step: {settings['up']}%",
                                      callback_data="up:change:call")
    down_percent = InlineKeyboardButton(text=f"Down step: {settings['down']}%",
                                        callback_data="down:change:call")
    high_percent = InlineKeyboardButton(text=f"High percent: {settings['high']}%",
                                        callback_data="high:change:call")
    volume_15_min = InlineKeyboardButton(text=f"Volume jump 15 min: {settings['volume_15_min']}%",
                                         callback_data="volume_15_min:change:call")
    volume_30_min = InlineKeyboardButton(text=f"Volume jump 30 min: {settings['volume_30_min']}%",
                                         callback_data="volume_30_min:change:call")

    buttons = [volume, start_percent, up_percent, down_percent, high_percent, volume_15_min, volume_30_min]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Values:", reply_markup=keyboard)


@dp.callback_query_handler(text_contains=":change:call")
async def change_volume(call: CallbackQuery, state: FSMContext):
    category = call.data.split(":")[0]
    buttons = ["Cancel set value"]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await call.message.answer(f"Set minimum value of {category}, which will boundary value", reply_markup=keyboard)
    await VolumeState.set_value.set()
    async with state.proxy() as data:
        data['category'] = category


@dp.message_handler(state=VolumeState.set_value)
async def set_volume(message: Message, state: FSMContext):
    if message.text == "Cancel set value":
        await state.reset_state()
        return await show_settings(message)
    data_container = await state.get_data()
    category = data_container["category"]
    is_right_value = await set_value_to_redis(category=category, value=message.text)
    if is_right_value:
        await state.reset_state()
        buttons = ['List of users', "Filter settings", "Admins settings", 'Back to user menu']
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*buttons)
        await message.answer(f"Boundary {category} {message.text} set successfully", reply_markup=keyboard)
        return await show_settings(message)
    else:
        await message.answer(f"Value {message.text} is wrong, set right value")
