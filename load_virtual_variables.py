import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("BOT_TOKEN")
MULTIPROCESS_CONFIG = os.getenv("MULTIPROCESSORING")
MAIN_ADMIN = int(os.getenv("SUPER_ADMIN_ID"))
DATABASE_ASYNC_URL = os.getenv("DATABASE_URL_ASYNC")
DATABASE_URL = os.getenv("DATABASE_URL")
WEBHOOK_PATH = f'{os.getenv("WEBHOOK_PATH")}{TOKEN}'
WEBAPP_HOST = os.getenv("WEBAPP_HOST")
BOT_PORT = os.getenv("BOT_PORT")
DOMAIN = os.getenv("DOMAIN_NAME")
WEBHOOK_URL = f"{DOMAIN}{WEBHOOK_PATH}"
