import os
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from asyncio import get_event_loop
from cache.redis_logic import RedisCache

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("BOT_TOKEN")
# __redis_url = os.getenv("REDIS_URL")
# __redis_port = os.getenv("REDIS_PORT")
# __redis_password = None

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=get_event_loop())
# CURRENCY_CONNECTION = RedisCache(host=__redis_url, port=__redis_port, db=0, password=__redis_password, timeout=120)
# VOLUME_CONNECTION = RedisCache(host=__redis_url, port=__redis_port, db=1, password=__redis_password, timeout=86400)
