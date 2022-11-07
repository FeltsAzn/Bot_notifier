from loader import bot
import time
import aiohttp
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
service_url = os.getenv("SERVICE_URL")


async def background_alerts():
    start_time = time.time()
    while True:
        async with aiohttp.ClientSession(service_url) as session:
            binance = await binance_info(session)
            kucoin = await kucoin_info(session)
            huobi = await huobi_info(session)
            okx = await okx_info(session)
            text = f"** {binance} **\n" \
                   f"** {kucoin} **\n" \
                   f"** {huobi} **\n" \
                   f"** {okx} **"
            info = counter_of_currencies(binance, kucoin, huobi, okx)
            text = ''
            for currency, price in info.items():
                text += f'{currency}:\n' \
                        f'Наименьшое значение - {price[0][0]} - {price[0][1]}\n' \
                        f'Наибольшоее значение  - {price[1][0]} - {price[1][1]}\n'\
                        f'Процентный разрыв валют {price[2]}'
            if text:
                await bot.send_message(chat_id=5703780641, text=text)
            await session.close()


def counter_of_currencies(binance: dict, kucoin: dict, huobi: dict, okx: dict):
    text = {}
    for currency, price in binance.items():
        result = quote_difference(price, kucoin[currency], huobi[currency], okx[currency])
        if float(result[2]) >= 0.005:
            text[currency] = result
    return text


def quote_difference(bin_price, kucoin_price, huobi_price, okx_price) -> tuple[list, list, str]:
    max_num: list = max(bin_price, kucoin_price, huobi_price, okx_price, key=lambda x: float(x[0]))
    min_num: list = min(bin_price, kucoin_price, huobi_price, okx_price, key=lambda x: float(x[0]))
    result = str(100 - float(min_num[0]) / float(max_num[0]) * 100)[:3]
    return min_num, max_num, result




async def binance_info(session: aiohttp.ClientSession) -> dict:
    async with session.get('/binance') as binance:
        binance = await binance.json()
    return binance


async def kucoin_info(session: aiohttp.ClientSession) -> dict:
    async with session.get('/kucoin') as kucoin:
        kucoin = await kucoin.json()
    return kucoin


async def huobi_info(session: aiohttp.ClientSession) -> dict:
    async with session.get('/huobi') as huobi:
        huobi = await huobi.json()
    return huobi


async def okx_info(session: aiohttp.ClientSession) -> dict:
    async with session.get('/okx') as okx:
        okx = await okx.json()
    return okx

