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
from alert_worker.handler_of_currency import counter_of_currencies
from alert_worker.template_fabric import content_creator
from alert_worker.alerts_exception_handler import exception_handler


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
    Обновление кэша при старте приложения или при добавлении нового пользователя
    """
    global USER_CACHE
    if multiproc_config.upper() == "ON":
        """Мультипроцессорное обновление кэша"""
        if instance.value:
            logger.info("CACHE HAS BEEN UPDATED")
            instance.value = False
            USER_CACHE = await Database().notifications_state()
    else:
        """Однопоточное обновление кэша"""
        USER_CACHE = await Database().notifications_state()
        logger.info("CACHE HAS BEEN UPDATED")


async def background_alerts(instance) -> None:
    """
    :param instance: multiprocessing.Value | bool
    Бесконечный цикл с запросами к биржам и отправке уведомлений пользователям
    """
    await update_user_cache(instance)
    try:
        while True:
            t1 = time.time()
            if not isinstance(instance, bool):
                # проверка на мультипроцессеринговый режим
                await update_user_cache(instance)
            raw_data = await data_collector()

            if time.time() - t1 < 1:
                logger.error("FastAPI service is dropped.")
                time.sleep(10)

            data = counter_of_currencies(*raw_data)
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
                await exception_handler(tg_id, bot)
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
