import time
import asyncio
import os
import sys
import multiprocessing
from dotenv import load_dotenv
from aiogram import executor
from handlers.middleware import update_users_list_sync
from loader import dp, bot
from alert_worker import alerts
from logger import logger
import handlers


def start_app_on_one_thread():
    try:
        dp.loop.create_task(alerts.background_alerts(True))
        executor.start_polling(dp, skip_updates=True)
    except ValueError as ex:
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
        executor.start_polling(dp, skip_updates=True, on_startup=update_users_list_sync(instance))
    except Exception as ex:
        logger.exception("Error process 1 (bot) "
                         f"exception type: {type(ex)} exception: {ex}")
        raise SystemExit


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

    if multiproc_config.upper() == "ON":
        logger.info("Start on multiprocessing mod")
        multiproc_app()
    else:
        logger.info("Start on one thread mod")
        start_app_on_one_thread()
