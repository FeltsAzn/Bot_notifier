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
    binan = {"NEARUSDT": 1, "TRXUSDT": 2, "BTCUSDT": 3, "ETHUSDT": 4, "APTUSDT": 5, "DOGEUSDT": 6}
    kuco = {"NEAR-BTC": 1,
            "TRX-BTC": 2,
            "USDT-BTC": 3,
            "ETH-BTC": 4,
            "APT-BTC": 5,
            "DOGE-BTC": 6}
    while True:
        async with aiohttp.ClientSession(service_url) as session:
            async with session.post('/binance', json=binan) as binance:
                binance = await binance.json()
            async with session.post('/kucoin', json=kuco) as kucoin:
                kucoin = await kucoin.json()
            text = f"** {binance}\n{kucoin} **"
            await bot.send_message(chat_id=5703780641, text=text)
            await session.close()
        time.sleep(1)

# TODO Обращение к сервису
