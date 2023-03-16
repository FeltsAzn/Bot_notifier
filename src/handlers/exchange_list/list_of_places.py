import asyncio
from aiogram.types import Message, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from utils.create_bot import dp
from utils.middleware import validate_user
from handlers.exchange_list.config_for_filling import fill_kb


@dp.message_handler(Text(equals="List of places"))
@validate_user
async def list_of_places(message: Message, is_user: bool):
    if is_user:
        keyboard = fill_kb.filling_keyboard()
        if fill_kb.last_page > 1:
            next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:places:call")
            stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
            keyboard.insert(stop_button)
            keyboard.insert(next_button)

        text = f"List of tracking exchanges (1/{fill_kb.last_page}):"
        await message.answer(text, reply_markup=keyboard)
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()

