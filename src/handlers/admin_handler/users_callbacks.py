import asyncio
from emoji import emojize
from aiogram.dispatcher.filters import Text
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           CallbackQuery,
                           ReplyKeyboardRemove,
                           Message,
                           ReplyKeyboardMarkup)
from handlers.admin_handler.config_for_filling import FillingUserTable
from utils.create_bot import dp, bot
from utils.middleware import get_user_from_tg_id, delete_user_from_tg_id, change_access
from utils.virtual_variables import MAIN_ADMIN
from utils.middleware import admin_validator

keyboard_instance = {}


def create_keyboard_instance(tg_id: int) -> None:
    keyboard_instance[tg_id] = FillingUserTable()


def get_keyboard_instance(tg_id: int) -> FillingUserTable:
    return keyboard_instance[tg_id]


@dp.message_handler(Text(equals="List of users"))
@admin_validator
async def start_list_of_users(message: Message):
    """Стартовый список пользователей"""
    create_keyboard_instance(message.from_user.id)
    fill_table = get_keyboard_instance(message.from_user.id)
    inline_keyboard = await fill_table()
    buttons = ["Back to admin panel"]
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    reply_keyboard.add(*buttons)
    await message.answer(text=emojize(":ledger:"), reply_markup=reply_keyboard)
    text = f"List of users (1/{fill_table.last_page}):"
    await message.answer(text, reply_markup=inline_keyboard)


@dp.callback_query_handler(text="next_page:user:call")
async def next_pages_handler(call: CallbackQuery):
    """Прокрутка списка пользователей вперёд"""
    fill_table = get_keyboard_instance(call.from_user.id)
    fill_table.up_values()
    keyboard = await fill_table()

    text = f"List of users ({fill_table.page_counter}/{fill_table.last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="back_page:user:call")
async def back_pages_handler(call: CallbackQuery):
    """Прокрутка списка пользователей назад"""
    fill_table = get_keyboard_instance(call.from_user.id)
    fill_table.down_values()
    keyboard = await fill_table()
    text = f"List of users ({fill_table.page_counter}/{fill_table.last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text_contains=":cancel:call")
async def list_of_users(call: CallbackQuery) -> None:
    """Filling is list of users after canceling action"""
    fill_table = get_keyboard_instance(call.from_user.id)
    keyboard = await fill_table()
    text = f"List of users ({fill_table.page_counter}/{fill_table.last_page}):"
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text_contains=":user:info:call")
async def user_info(call: CallbackQuery) -> None:
    """Получение информации по конкретному пользователю"""
    user_tg_id = int(call.data.split(':')[0])
    user = await get_user_from_tg_id(user_tg_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    text = f"<i>tg_id</i>: <b>{user_tg_id}</b>\n" \
           f"<i>name</i>: <b>{user['username']}</b>\n" \
           f"<i>notify</i>: <b>{user['state']}</b>\n" \
           f"<i>status</i>: <b>{user['access']}</b>\n"
    delete_but = InlineKeyboardButton(text="Delete user",
                                      callback_data=f"{user_tg_id}:ask:delete:call")
    change_access_but = InlineKeyboardButton(text="Change access",
                                             callback_data=f"{user_tg_id}:{user['access']}:change_access:call")
    cancel_but = InlineKeyboardButton(text="Cancel",
                                      callback_data=f"{user_tg_id}:cancel:call")
    keyboard.add(delete_but, change_access_but, cancel_but)

    await call.message.edit_text(text, reply_markup=keyboard, parse_mode='html')


@dp.callback_query_handler(text_contains=":change_access:call")
async def change_user_access(call: CallbackQuery) -> None:
    """Changing user access"""
    data = call.data.split(':')
    user_tg_id = int(data[0])
    user_access = data[1]
    keyboard = InlineKeyboardMarkup(row_width=1)
    match user_access:
        case "ADMIN":
            change_but = InlineKeyboardButton(text="Down user access", callback_data=f"{user_tg_id}:make_user:call")
        case _:
            change_but = InlineKeyboardButton(text="Up to admin access", callback_data=f"{user_tg_id}:make_admin:call")

    cancel_but = InlineKeyboardButton(text="Cancel", callback_data=f"{user_tg_id}:user:info:call")
    keyboard.add(change_but, cancel_but)
    await call.message.edit_text(text="Choose user access", reply_markup=keyboard, parse_mode="html")


@dp.callback_query_handler(text_contains=":make_user:call")
async def downgrade_to_user_access(call: CallbackQuery):
    user_tg_id = int(call.data.split(':')[0])


    if user_tg_id == MAIN_ADMIN:
        mes = "This is main admin. You can't change his access."
    else:
        if user_tg_id != call.from_user.id:

            is_changed = await change_access(tg_id=user_tg_id, access="USER")
            if is_changed:
                mes = f"User {user_tg_id} access downgrade to user."
                await bot.send_message(chat_id=user_tg_id,
                                       text="Your access downgraded. You are user.\nSend /start to load a keyboard.",
                                       reply_markup=ReplyKeyboardRemove())
            else:
                mes = f"Error on downgrade access for user {user_tg_id}."

        else:
            mes = "Don't downgrade your access."

    fill_table = get_keyboard_instance(call.from_user.id)
    keyboard = await fill_table()
    text = f"List of users ({fill_table.page_counter}/{fill_table.last_page}):"
    await call.message.edit_text(mes)
    await asyncio.sleep(2)
    await call.message.edit_text(text, reply_markup=keyboard, parse_mode="html")


@dp.callback_query_handler(text_contains=":make_admin:call")
async def elevate_to_admin_access(call: CallbackQuery):
    user_tg_id = int(call.data.split(':')[0])

    if user_tg_id != call.from_user.id:
        is_changed = await change_access(tg_id=user_tg_id, access="ADMIN")
        if is_changed:
            mes = f"User {user_tg_id} access upgraded to user"
            await bot.send_message(chat_id=user_tg_id,
                                   text="Your access upgraded. You are admin!\nSend /start to update keyboard.",
                                   reply_markup=ReplyKeyboardRemove())
        else:
            mes = f"Error on upgrade access for user {user_tg_id} "
    else:
        mes = "Your have ADMIN access already."

    fill_table = get_keyboard_instance(call.from_user.id)
    keyboard = await fill_table()
    text = f"List of users ({fill_table.page_counter}/{fill_table.last_page}):"
    await call.message.edit_text(mes)
    await asyncio.sleep(2)
    await call.message.edit_text(text, reply_markup=keyboard, parse_mode="html")


@dp.callback_query_handler(text_contains=":ask:delete:call")
async def ask_delete_user(call: CallbackQuery) -> None:
    """Deleting the selected user solution"""

    user_tg_id = int(call.data.split(':')[0])

    keyboard = InlineKeyboardMarkup(row_width=1)
    delete_but = InlineKeyboardButton(text="Yes, delete", callback_data=f"{user_tg_id}:delete:call")
    cancel_but = InlineKeyboardButton(text="Cancel", callback_data=f"{user_tg_id}:user:info:call")
    keyboard.add(delete_but, cancel_but)

    await call.message.edit_text(text="Are you sure to delete user?", reply_markup=keyboard, parse_mode="html")


@dp.callback_query_handler(text_contains=":delete:call")
async def delete_user(call: CallbackQuery) -> None:
    """Deleting the selected user"""

    user_tg_id = int(call.data.split(':')[0])

    if user_tg_id != call.from_user.id:
        is_deleted: bool = await delete_user_from_tg_id(user_tg_id)
        if is_deleted:
            mes = f"User {user_tg_id} removed"
        else:
            mes = f"Error on removing user {user_tg_id}"
    else:
        mes = "Don't delete yourself\nlike that."

    fill_table = get_keyboard_instance(call.from_user.id)
    keyboard = await fill_table()

    text = f"List of users ({fill_table.page_counter}/{fill_table.last_page}):"
    await call.message.edit_text(mes)
    await asyncio.sleep(2)
    await call.message.edit_text(text, reply_markup=keyboard, parse_mode="html")
