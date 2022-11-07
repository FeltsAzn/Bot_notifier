from loader import bot
import asyncio
import time
import aiohttp
import random
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
service_url = os.getenv("SERVICE_URL")


async def background_alerts():
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
            print(text)
            # await bot.send_message(chat_id=5703780641, text=text)
            await session.close()
        time.sleep(1)
        break


async def binance_info(session: aiohttp.ClientSession) -> dict:
    binance_currency = {"NEARUSDT": 1,
                        "TRXUSDT": 2,
                        "BTCUSDT": 3,
                        "ETHUSDT": 4,
                        "APTUSDT": 5,
                        "DOGEUSDT": 6}
    async with session.post('/binance', json=binance_currency) as binance:
        binance = await binance.json()
    return binance


async def kucoin_info(session: aiohttp.ClientSession) -> dict:
    kucoin_currency = {"NEAR": 1,
                       "TRX": 2,
                       "USDT": 3,
                       "ETH": 4,
                       "APT": 5,
                       "DOGE": 6}

    async with session.post('/kucoin', json=kucoin_currency) as kucoin:
        kucoin = await kucoin.json()
    return kucoin


async def huobi_info(session: aiohttp.ClientSession) -> dict:
    huobi_currency = {"nearusdt": 1,
                      "trxusdt": 2,
                      "btcusdt": 3,
                      "ethusdt": 4,
                      "aptusdt": 5,
                      "waxlusdt": 6,
                      "dogeusdt": 7}
    async with session.post('/huobi', json=huobi_currency) as huobi:
        huobi = await huobi.json()
    return huobi


async def okx_info(session: aiohttp.ClientSession) -> dict:
    okx_currency = {"NEAR-USDT": 1,
                    "TRX-USDT": 2,
                    "BTC-USDT": 3,
                    "ETH-USDT": 4,
                    "APT-USDT": 5,
                    "DOGE-USDT": 6}
    async with session.post('/okx', json=okx_currency) as okx:
        okx = await okx.json()
    return okx

