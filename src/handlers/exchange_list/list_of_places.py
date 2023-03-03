import asyncio
from aiogram.types import Message, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from loader import dp
from handlers.exchange_list.config_for_filling import last_page, filling_keyboard
from middleware import validate_user


@dp.message_handler(Text(equals="List of places"))
@validate_user
async def list_of_places(message: Message, is_user: bool):
    if is_user:
        keyboard = filling_keyboard()
        if last_page > 1:
            next_button = InlineKeyboardButton(text=">>>>>", callback_data="next_page:places:call")
            stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
            keyboard.insert(stop_button)
            keyboard.insert(next_button)

        text = f"List of tracking exchanges (1/{last_page}):"
        await message.answer(text, reply_markup=keyboard)
    else:
        msg_id = await message.answer("You are not registered. Send /start for registration")
        await asyncio.sleep(2)
        await msg_id.delete()

