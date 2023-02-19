import time
import aiohttp
import asyncio
import os
from emoji import emojize
from aiogram.utils import markdown, exceptions
from db.crud import Database
from loader import bot
from logger import logger
from alert_worker import http_req
from alert_worker.template_fabric import content_creator
from alert_worker.alerts_exception_handler import UnexpectedException
from alert_worker.exchanges_cache.quotes_of_currency_cache import CurrencyCache


"""
Файл alerts.py предназначен для уведомления позльзователей о изменении цен на бирже.
Используется бесконечный цикл для постоянной работы бота.
"""


service_url = os.getenv("SERVICE_URL")
multiproc_config = os.getenv("MULTIPROCESSORING")

USER_CACHE = []


async def update_user_cache(instance) -> None:
    """
    :param instance: multiprocessing.Value | bool
    Updating cache after app launching or after adding new user
    """
    global USER_CACHE
    if multiproc_config.upper() == "ON":
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
            raw_data = await data_collector()

            if time.time() - t1 < 1:
                logger.error("FastAPI service is dropped.")
                await bot.send_message()
                time.sleep(10)

            data = CurrencyCache().counter_of_currencies_redis(*raw_data)
            content: list = content_creator(data)


            if content != [] and USER_CACHE != []:
                for tg_id, state in USER_CACHE:
                    if state == "ACTIVATED":
                        try:
                            await bot.send_message(chat_id=tg_id,
                                                   text=emojize(markdown.text(*content), language="alias"),
                                                   parse_mode="html")
                        except exceptions.BotBlocked as ex:
                            logger.warning(f"Message didn't send to user {tg_id}. {ex}")

    except (TypeError, AttributeError) as ex:
        logger.exception(f"Exception on alerts loop: {ex}")
        for tg_id, state in USER_CACHE:
            if state == "ACTIVATED":
                error = UnexpectedException(tg_id, bot)
                await error.exception_handler()
            raise SystemError


async def data_collector() -> tuple:
    """Сборщик данных с различных бирж"""
    async with aiohttp.ClientSession(service_url) as session:
        list_of_exchanges = [
            "binance",
            "kucoin",
            "huobi",
            "okx"
        ]
        tasks = []
        for exchange in list_of_exchanges:
            request = http_req.get_exchange_data(session, exchange)
            tasks.append(request)
        all_data = await asyncio.gather(*tasks)
    return all_data
