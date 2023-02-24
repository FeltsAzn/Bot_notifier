from aiogram import Dispatcher, Bot
from asyncio import get_event_loop
from load_virtual_variables import TOKEN


bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=get_event_loop())
