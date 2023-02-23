import time
import asyncio
import os
import sys
import multiprocessing

from handlers.main_handler import register_admin_handlers

from aiogram.utils.exceptions import NetworkError
from dotenv import load_dotenv
from aiogram.utils.executor import start_webhook
from aiogram import executor
from handlers.middleware import update_users_list_sync
from loader import dp, bot
from alert_worker import alerts
from logger import logger


def start_app_on_one_thread():
    try:
        dp.loop.create_task(alerts.background_alerts(True))
        executor.start_polling(dp, skip_updates=True)
    except (SystemExit, ) as ex:
        logger.exception("Stop one thread app."
                         f"exception type: {type(ex)} exception: {ex}")
        bot.close()


def multiproc_app():
    manager = multiprocessing.Manager()
    instance = manager.Value("instance", False)
    process_1 = multiprocessing.Process(target=start_bot_proc1, args=(instance,))
    process_2 = multiprocessing.Process(target=start_alerts_proc2, args=(instance,))
    process_1.start()
    process_2.start()

    while True:
        time.sleep(3)
        if not process_1.is_alive() or not process_2.is_alive():
            ex = "process 1 (telegram bot) was closed with exception"
            if process_1.is_alive():
                ex = "process 2(alerts loop) was closed with exception"

            process_1.terminate()
            process_2.terminate()
            logger.exception("Stop multiprocessing app. "
                             f"last exception: {ex}")
            print("BOT STOPPED", file=sys.stderr)
            sys.exit(13)


def start_bot_proc1(instance):
    """Запуск бота в процессе 1"""
    try:
        update_users_list_sync(instance)
        WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
        WEBAPP_HOST = os.getenv("WEBAPP_HOST")
        BOT_PORT = os.getenv("BOT_PORT")
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            on_startup= on_startup,
            host=WEBAPP_HOST,
            port=BOT_PORT,
        )


    except NetworkError as ex:
        logger.exception("Error process 1 (bot) "
                         f"exception type: {type(ex)} exception: {ex}")
        raise SystemExit

async def on_startup(dp):
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    register_admin_handlers(dp)
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


def start_alerts_proc2(instance):
    """Запуск уведомлений в процессе 2"""
    try:
        asyncio.run(alerts.background_alerts(instance))
    except SystemError as ex:
        logger.exception("Error process 2 (alerts) "
                         f"exception type: {type(ex)} exception: {ex}")
        raise SystemExit


if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    multiproc_config = os.getenv("MULTIPROCESSORING")

    match multiproc_config.upper():
        case "ON":
            logger.info("Start on multiprocessing mod")
            multiproc_app()
        case _:
            logger.info("Start on one thread mod")
            start_app_on_one_thread()
