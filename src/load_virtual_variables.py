import os
from dotenv import load_dotenv
from cache.async_redis_logic import AsyncRedisCache

dotenv_path = os.path.join(os.path.dirname(__file__), ".env.internal.bot")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("BOT_TOKEN")
BOT_PORT = os.getenv("BOT_PORT")
MAIN_ADMIN = int(os.getenv("SUPER_ADMIN_ID"))
DATABASE_ASYNC_URL = os.getenv("DATABASE_URL_ASYNC")

WEBHOOK_PATH = f'{os.getenv("WEBHOOK_BASE_PATH")}/{TOKEN}'
WEBAPP_HOST = os.getenv("WEBAPP_HOST")
DOMAIN = os.getenv("DOMAIN_NAME")
WEBHOOK_URL = f"{DOMAIN}{WEBHOOK_PATH}"

BASE_MINIMUM_VOLUME = 100000
__redis_url = os.getenv("REDIS_URL")
__redis_port = os.getenv("REDIS_PORT")
__redis_password = os.getenv("REDIS_PASS")
REDIS_ASYNC_CONN = AsyncRedisCache(host=__redis_url, port=__redis_port, db=2, password=__redis_password)
LOAD_BTC_ETH_PRICE = AsyncRedisCache(host=__redis_url, port=__redis_port, db=4, password=__redis_password)
