import asyncio
import os
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from loader import dp
from handlers.admin_handler.config_for_filling import filling_keyboard, last_page
from handlers.admin_handler.page_switch_users import page_counter
from handlers.middleware import get_user_from_tg_id, delete_user_from_tg_id

"""
Файл users_actioins_callback.py предназначен для реализации функционала бота "Админка -> Список пользователей".
Основные кнопки - инлайн, реализуется вывод информации о пользователе и возможность его удаления из БД . 
"""

super_admin_id = os.getenv("SUPER_ADMIN_ID")


@dp.callback_query_handler(text_contains=":cancel:call")
async def list_of_users(call: CallbackQuery) -> None:
    """заполниние списка пользователей после отмены действия"""

    keyboard = await filling_keyboard()
    if page_counter > 1:
        next_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        stop_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
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
async def user_info(call: CallbackQuery) -> None:
    """получение информации по конкретному пользователю"""
    user_tg_id = int(call.data.split(':')[0])
    _, username, state, status = await get_user_from_tg_id(user_tg_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    text = f"<i>tg_id</i>: <b>{user_tg_id}</b>\n" \
           f"<i>name</i>: <b>{username}</b>\n" \
           f"<i>notify</i>: <b>{state}</b>\n" \
           f"<i>status</i>: <b>{status}</b>\n"
    delete_but = InlineKeyboardButton(text="Удалить пользователя", callback_data=f"{user_tg_id}:ask:delete:call")
    cancel_but = InlineKeyboardButton(text="Отмена", callback_data=f"{user_tg_id}:cancel:call")
    keyboard.insert(delete_but)
    keyboard.insert(cancel_but)

    await call.message.edit_text(text, reply_markup=keyboard, parse_mode='html')


@dp.callback_query_handler(text_contains=":ask:delete:call")
async def ask_delete_user(call: CallbackQuery) -> None:
    """Выбор удаления выбранного пользователя"""

    user_tg_id = int(call.data.split(':')[0])

    keyboard = InlineKeyboardMarkup(row_width=1)
    delete_but = InlineKeyboardButton(text="Да, удалить", callback_data=f"{user_tg_id}:delete:call")
    cancel_but = InlineKeyboardButton(text="Отмена", callback_data=f"{user_tg_id}:user:info:call")
    keyboard.insert(delete_but)
    keyboard.insert(cancel_but)

    await call.message.edit_text(text="Вы действительно хотите\n"
                                      "удалить пользователя?", reply_markup=keyboard, parse_mode="html")


@dp.callback_query_handler(text_contains=":delete:call")
async def delete_user(call: CallbackQuery) -> None:
    """Удаление выбранного пользователя"""

    user_tg_id = int(call.data.split(':')[0])

    if user_tg_id != call.from_user.id:
        state: bool = await delete_user_from_tg_id(user_tg_id)
        if state:
            mes = f"Пользователь {user_tg_id} удален"
        else:
            mes = f"Ошибка удаления пользователя {user_tg_id}"
    else:
        mes = "Не нужно удалять самого себя\nтаким образом."

    keyboard_without_but = await filling_keyboard()
    keyboard = inserting_button(keyboard_without_but)

    text = f"Список пользователей ({page_counter}/{last_page}):"
    await call.message.edit_text(mes)
    await asyncio.sleep(2)
    await call.message.edit_text(text, reply_markup=keyboard, parse_mode="html")


def inserting_button(keyboard: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    if page_counter == last_page and last_page != 1:
        right_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
        keyboard.insert(right_button)
        keyboard.insert(left_button)
    elif page_counter > 1 and last_page != 2:
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        left_button = InlineKeyboardButton(text="<<<", callback_data="back_page:user:call")
        keyboard.insert(right_button)
        keyboard.insert(left_button)
    elif last_page > 1 and page_counter == 1:
        right_button = InlineKeyboardButton(text=">>>", callback_data="next_page:user:call")
        left_button = InlineKeyboardButton(text="|||", callback_data="stop:call")
        keyboard.insert(right_button)
        keyboard.insert(left_button)
    return keyboard
