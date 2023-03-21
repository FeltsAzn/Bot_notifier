import os
from dotenv import load_dotenv
from utils.async_redis_cache import AsyncRedisCache

dotenv_path = os.path.join(os.path.dirname(__file__), ".env.internal.bot")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# BOT VARIABLES
TOKEN = os.getenv("BOT_TOKEN")
BOT_PORT = os.getenv("BOT_PORT")
MAIN_ADMIN = int(os.getenv("SUPER_ADMIN_ID"))
WEBHOOK_PATH = f'{os.getenv("WEBHOOK_BASE_PATH")}/{TOKEN}'
WEBAPP_HOST = os.getenv("WEBAPP_HOST")
DOMAIN = os.getenv("DOMAIN_NAME")
WEBHOOK_URL = f"{DOMAIN}{WEBHOOK_PATH}"

# MONGO VARIABLES
__mongo_add = os.getenv("MONGO_ADDRESS")
__mongo_port = os.getenv("MONGO_PORT")
__mongo_user = os.getenv("MONGO_USER")
__mongo_pass = os.getenv("MONGO_PASSWORD")
DATABASE_URL = f"mongodb://{__mongo_user}:{__mongo_pass}@{__mongo_add}:{__mongo_port}/"

# REDIS VARIABLES
__redis_url = os.getenv("REDIS_URL")
__redis_port = os.getenv("REDIS_PORT")
__redis_password = os.getenv("REDIS_PASS")
REDIS_ASYNC_CONN = AsyncRedisCache(host=__redis_url, port=__redis_port, db=2, password=__redis_password)
LOAD_SETTINGS = AsyncRedisCache(host=__redis_url, port=__redis_port, db=4, password=__redis_password)
