from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from loader import dp
from aiogram.dispatcher.filters import Text
from db.crud import Database
from keyboards.inline.item_list import callback


@dp.message_handler(Text(equals="Список площадок"))
async def start(message: Message):
    buttons = ["<<< Назад", 'Далее >>>', 'Домой']
    keyboard = InlineKeyboardMarkup()
    items: list = await Database().get_services()
    for item in items:
        button = InlineKeyboardButton(text=item, callback_data=callback.new(item_name=item, action='select'))
        keyboard.insert(button)
    keyboard.add(*buttons)
    await message.answer("Список площадок:", reply_markup=keyboard)


# @dp.callback_query_handlers(text_contains="select")
# async def choose_service(callback: CallbackQuery):
#     pass
#     # TODO Сделать обработку callback
