from loader import bot
import aiohttp
import os
from dotenv import load_dotenv
from db.crud import Database
from decimal import Decimal
from alert_worker import http_req


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
    await update_user_cache()
    global USER_CACHE
    """Бесконечный цикл с запросами к биржам и отправке уведомлений"""
    while True:
        async with aiohttp.ClientSession(service_url) as session:
            binance = await http_req.binance_info(session)
            kucoin = await http_req.kucoin_info(session)
            huobi = await http_req.huobi_info(session)
            okx = await http_req.okx_info(session)

        info = counter_of_currencies(binance, kucoin, huobi, okx)
        text = ''
        for currency, price in info.items():
            text += create_template(currency, price)
        if text:
            for tg_id, _ in USER_CACHE:
                await bot.send_message(chat_id=tg_id, text=text)
        await session.close()


def create_template(currency: str, price: tuple) -> str:
    """Метод создания шаблона сообщения для уведомления"""
    minimum, maximum, percent = price
    min_val, min_coin = minimum
    max_val, max_coin = maximum
    text = f'{currency}:\n' \
           f'Наименьшее: {str(min_val)[:8]}$ - {min_coin}\n' \
           f'Наибольшее: {str(max_val)[:8]}$ - {max_coin}\n' \
           f'Разница в {percent}%\n\n'
    return text


def counter_of_currencies(binance: dict, kucoin: dict, huobi: dict, okx: dict) -> dict:
    """Обработчик отсеивания не рентабельных данных"""
    data = {}
    for currency, price in binance.items():
        result = quote_difference(price, kucoin[currency], huobi[currency], okx[currency])
        if float(result[2]) >= 0.5:
            data[currency] = result
    return data


def quote_difference(bin_price, kucoin_price, huobi_price, okx_price) -> tuple[list, list, str]:
    """Высчитывание наименьшего и наибольшего значения"""
    max_num: list = max(bin_price, kucoin_price, huobi_price, okx_price, key=lambda x: float(x[0]))
    min_num: list = min(bin_price, kucoin_price, huobi_price, okx_price, key=lambda x: float(x[0]))
    result = str(100 - Decimal(min_num[0]) / Decimal(max_num[0]) * 100)[:4]
    return min_num, max_num, result




