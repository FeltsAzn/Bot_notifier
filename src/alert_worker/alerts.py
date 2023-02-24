import time
import redis
from emoji import emojize
from aiogram.utils import markdown, exceptions
from aiohttp.client_exceptions import ClientConnectorError
from src.db.crud import Database
from src.loader import bot
from src.logger import logger
from src.alert_worker import http_req
from src.alert_worker.alerts_exception_handler import UnexpectedException
from load_virtual_variables import MULTIPROCESS_CONFIG, MAIN_ADMIN

"""
Файл alerts.py предназначен для уведомления позльзователей о изменении цен на бирже.
Используется бесконечный цикл для постоянной работы бота.
"""



USER_CACHE = []


async def update_user_cache(instance) -> None:
    """
    :param instance: multiprocessing.Value | bool
    Updating cache after app launching or after adding new user
    """
    global USER_CACHE
    if MULTIPROCESS_CONFIG.upper() == "ON":
        """Updating cache in multiprocess mod"""
        if instance.value:
            logger.info("CACHE HAS BEEN UPDATED")
            instance.value = False
            USER_CACHE = await Database().notifications_state()
    else:
        """Updating cache in one thread mod"""
        USER_CACHE = await Database().notifications_state()
        logger.info("CACHE HAS BEEN UPDATED")


async def background_alerts(instance) -> None:
    """
    :param instance: multiprocessing.Value | bool
    Mainloop with requests to backend and sending notifications to telegram users
    """
    await update_user_cache(instance)
    try:
        while True:
            t1 = time.time()
            if not isinstance(instance, bool):
                # verification on multiprocess mod
                await update_user_cache(instance)
            raw_data = await http_req.exchanges_data_collector()

            if time.time() - t1 < 1:
                logger.error("FastAPI service is dropped.")
                await bot.send_message(chat_id=MAIN_ADMIN, text="FastAPI service is dropped.")
                time.sleep(10)

            content = await http_req.give_finished_text(*raw_data)

            await send_message(content)

    except ClientConnectorError:
        time.sleep(10)
        logger.exception("Telegram connection refused. Timeout 10 second activated")


    except (TypeError, AttributeError, redis.exceptions.ConnectionError) as ex:
        logger.exception(f"Exception on alerts loop: {ex}")
        for tg_id, state in USER_CACHE:
            if state == "ACTIVATED":
                error = UnexpectedException(tg_id, bot)
                await error.exception_handler()
            raise SystemError

async def send_message(content: list):
    if content != [] and USER_CACHE != []:
        for tg_id, state in USER_CACHE:
            if state == "ACTIVATED":
                try:
                    await bot.send_message(chat_id=tg_id,
                                           text=emojize(markdown.text(*content), language="alias"),
                                           parse_mode="html")
                except exceptions.BotBlocked as ex:
                    logger.warning(f"Message didn't send to user {tg_id}. {ex}")
                    await bot.send_message(chat_id=MAIN_ADMIN, text=f"Message not sent to user {tg_id}. He is blocked bot")