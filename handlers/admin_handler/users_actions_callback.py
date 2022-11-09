import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from loader import dp
from db.crud import Database
from handlers.admin_handler.config_for_filling import filling_keyboard, last_page
from handlers.admin_handler.page_switch_users import page_counter


@dp.callback_query_handler(text_contains=":cancel:call")
async def list_of_users(call: CallbackQuery):
    """заполниние списка пользователей после отмены действия"""

    keyboard = await filling_keyboard()
    if page_counter > 1:
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="<<<", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)
    elif last_page > 1:
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)
    text = f"Список пользователей ({page_counter}/{last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text_contains=":user:info:call")
async def user_info(call: CallbackQuery):
    """получение информации по конкретному пользователю"""
    user_tg_id = int(call.data.split(':')[0])
    _, username, state = await Database().get_user(user_tg_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    text = f'<i>tg_id</i>: <b>{user_tg_id}</b>\n' \
           f'<i>name</i>: <b>{username}</b>\n' \
           f'<i>notify</i>: <b>{state}</b>'
    delete_but = InlineKeyboardButton(text="Удалить пользователя", callback_data=f"{user_tg_id}:ask:delete:call")
    cancel_but = InlineKeyboardButton(text="Отмена", callback_data=f"{user_tg_id}:cancel:call")
    keyboard.insert(delete_but)
    keyboard.insert(cancel_but)

    await call.message.edit_text(text, reply_markup=keyboard, parse_mode='html')


@dp.callback_query_handler(text_contains=":ask:delete:call")
async def ask_delete_user(call: CallbackQuery):
    """Выбор удаления выбранного пользователя"""

    user_tg_id = int(call.data.split(':')[0])

    keyboard = InlineKeyboardMarkup(row_width=1)
    delete_but = InlineKeyboardButton(text="Да, удалить", callback_data=f"{user_tg_id}:delete:call")
    cancel_but = InlineKeyboardButton(text="Отмена", callback_data=f"{user_tg_id}:user:info:call")
    keyboard.insert(delete_but)
    keyboard.insert(cancel_but)

    await call.message.edit_text(text="Вы действительно хотите\n"
                                           "удалить пользователя?", reply_markup=keyboard, parse_mode='html')


@dp.callback_query_handler(text_contains=":delete:call")
async def ask_delete_user(call: CallbackQuery):
    """Удаление выбранного пользователя"""

    user_tg_id = int(call.data.split(':')[0])
    if user_tg_id != call.from_user.id:
        state = await Database().delete_user(user_tg_id)
        if state:
            mes = "Пользователь удален"
        else:
            mes = "Ошибка удаления"
    else:
        mes = "Не нужно удалять самого себя\nтаким образом."

    keyboard = await filling_keyboard()
    if page_counter > 1:
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="<<<", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)
    elif last_page > 1:
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(stop_button)
        keyboard.insert(next_button)
    text = f"Список пользователей ({page_counter}/{last_page}):"
    await call.message.edit_text(mes)
    await asyncio.sleep(2)
    await call.message.edit_text(text, reply_markup=keyboard, parse_mode='html')




