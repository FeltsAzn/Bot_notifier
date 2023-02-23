import os
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from asyncio import get_event_loop

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=get_event_loop())
