import time
import asyncio
import sys
import multiprocessing
import aiogram
import handlers
from aiogram.utils.exceptions import NetworkError
from aiogram.utils.executor import start_webhook
from alert_worker.alerts import NotificationAlerter
from utils.create_bot import dp, bot
from utils.logger import logger
from utils.virtual_variables import (WEBHOOK_PATH,
                                     WEBHOOK_URL,
                                     WEBAPP_HOST,
                                     BOT_PORT,
                                     LOAD_BTC_ETH_PRICE,
                                     BASE_MINIMUM_VOLUME)


def start():
    process_1 = multiprocessing.Process(target=start_bot_proc1)
    process_2 = multiprocessing.Process(target=start_alerts_proc2)
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


def start_bot_proc1():
    """Запуск бота в процессе 1"""
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
    except NetworkError as ex:
        logger.exception("Error process 1 (bot) "
                         f"exception type: {type(ex)} exception: {ex}")
        raise SystemExit


async def on_startup(dp: aiogram.Dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    info = await bot.get_webhook_info()
    logger.info("Webhook is created. Bot is running")
    logger.info(f"Webhook info: {info}")
    async with LOAD_BTC_ETH_PRICE as session:
        await session.create_key_and_value("MINIMUM_VOLUME", BASE_MINIMUM_VOLUME)


async def on_shutdown(dp: aiogram.Dispatcher):
    await bot.delete_webhook()
    logger.info("Webhook is deleted. Bot is stopped")


def start_alerts_proc2():
    """Run notifications in second process"""
    try:
        notification = NotificationAlerter()
        asyncio.run(notification.background_task())
    except SystemError as ex:
        logger.exception("Error process 2 (alerts) "
                         f"exception type: {type(ex)} exception: {ex}")
        raise SystemExit


if __name__ == "__main__":
    logger.info("Start app")
    start()
