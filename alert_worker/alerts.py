import aiohttp
import os
from dotenv import load_dotenv
from emoji import emojize
from aiogram.utils import markdown
from loader import bot
from db.crud import Database
from alert_worker import http_req
from alert_worker.handler_of_currency import counter_of_currencies
from alert_worker.template_fabric import content_creator


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
service_url = os.getenv("SERVICE_URL")


USER_CACHE = []


async def update_user_cache() -> None:
    """Обновление кэша при старте приложения и добавления нового пользователя"""
    global USER_CACHE
    USER_CACHE = await Database().get_users()


async def background_alerts() -> None:
    """Бесконечный цикл с запросами к биржам и отправке уведомлений"""
    await update_user_cache()
    global USER_CACHE

    while True:
        async with aiohttp.ClientSession(service_url) as session:
            binance = await http_req.binance_info(session)
            kucoin = await http_req.kucoin_info(session)
            huobi = await http_req.huobi_info(session)
            okx = await http_req.okx_info(session)

        data: dict[str:tuple[tuple, str]] = counter_of_currencies(binance, kucoin, huobi, okx)

        content: list = content_creator(data)

        if content:
            # for tg_id, _ in USER_CACHE:
            #     await bot.send_message(chat_id=tg_id,
            #                            text=emojize(markdown.text(*content), language='alias'),
            #                            parse_mode='html')
            await bot.send_message(chat_id=5703780641,
                                   text=emojize(markdown.text(*content), language='alias'),
                                   parse_mode='html')
        await session.close()






