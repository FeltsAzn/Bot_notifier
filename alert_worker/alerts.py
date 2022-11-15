import multiprocessing
import time
import aiohttp
import asyncio
import os
from dotenv import load_dotenv
from emoji import emojize
from aiogram.utils import markdown
from loader import bot
from db.crud import Database
from alert_worker import http_req
from alert_worker.handler_of_currency import counter_of_currencies
from alert_worker.template_fabric import content_creator
from alert_worker.alerts_exception_handler import exception_handler
from logger import logger

"""
Файл alerts.py предназначен для уведомления позльзователей о изменении цен на бирже.
Используется бесконечный цикл для постоянной работы бота.
"""


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
service_url = os.getenv("SERVICE_URL")
multiproc_config = os.getenv("MULTIPROCESSORING")

USER_CACHE = []


async def update_user_cache(instance: multiprocessing.Value or bool) -> None:
    """Обновление кэша при старте приложения или при добавлении нового пользователя"""
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


async def background_alerts(instance: multiprocessing.Value or bool) -> None:
    """Бесконечный цикл с запросами к биржам и отправке уведомлений пользователям"""
    await update_user_cache(instance)
    try:
        while True:
            t1 = time.time()

            if not isinstance(instance, bool):
                # проверка на мультипроцессеринговый режим
                await update_user_cache(instance)
            raw_data = await data_collector()
            if time.time() - t1 < 1:
                # проверк на случай когда сервер fastapi не будет отвечать
                time.sleep(10)
            if raw_data:
                data = counter_of_currencies(*raw_data)
                content: list = content_creator(data)

                if content != [] and USER_CACHE != []:
                    for tg_id, state in USER_CACHE:
                        if state == "ACTIVATED":
                            await bot.send_message(chat_id=tg_id,
                                                   text=emojize(markdown.text(*content), language='alias'),
                                                   parse_mode='html')
            else:
                logger.error("FastAPI service is dropped.")

    except Exception as ex:
        logger.exception(f"Exception on alerts loop: {ex}")
        for tg_id, state in USER_CACHE:
            if state == "ACTIVATED":
                await exception_handler(tg_id, bot)
            raise ex


async def data_collector() -> list:
    """Сборщик данных с различных бирж"""
    async with aiohttp.ClientSession(service_url) as session:
        list_of_requests = [
            http_req.binance_info(session),
            http_req.kucoin_info(session),
            http_req.huobi_info(session)
        ]
        # http_req.okx_info(session)
        tasks = list(map(lambda x: asyncio.wait_for(x, timeout=5), list_of_requests))
        try:
            all_data = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as ex:
            logger.exception(f"Exception on gather loop on http-requests: {ex}")
            all_data = []
    all_data = list(filter(lambda x: isinstance(x, dict), all_data))
    return all_data


