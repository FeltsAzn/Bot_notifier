import time
import asyncio
import sys
import multiprocessing
import aiogram
from aiogram.utils.exceptions import NetworkError
from aiogram.utils.executor import start_webhook
from src.handlers.middleware import update_users_list_sync
from src import handlers
from src.loader import dp, bot
from src.alert_worker import alerts
from src.logger import logger
from load_virtual_variables import WEBHOOK_PATH, WEBHOOK_URL, WEBAPP_HOST, BOT_PORT



def start_app_on_one_thread():
    try:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            on_startup=on_startup,
            host=WEBAPP_HOST,
            port=BOT_PORT,
            on_shutdown=on_shutdown,
        )
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
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            on_startup= on_startup,
            host=WEBAPP_HOST,
            port=BOT_PORT,
            on_shutdown=on_shutdown,
        )
    except NetworkError as ex:
        logger.exception("Error process 1 (bot) "
                         f"exception type: {type(ex)} exception: {ex}")
        raise SystemExit

async def on_startup(dp: aiogram.Dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    logger.info("Webhook is created. Bot is running")

async def on_shutdown(dp: aiogram.Dispatcher):
    await bot.delete_webhook()
    logger.info("Webhook is deleted. Bot is stopped")


def start_alerts_proc2(instance):
    """Run notifications in second process"""
    try:
        asyncio.run(alerts.background_alerts(instance))
    except SystemError as ex:
        logger.exception("Error process 2 (alerts) "
                         f"exception type: {type(ex)} exception: {ex}")
        raise SystemExit
