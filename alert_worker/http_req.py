import aiohttp
from logger import logger
import asyncio
"""
Файл http_req.py - запросы к endpoint'ам приложения на FastAPI
"""


async def get_exchange_data(session: aiohttp.ClientSession, service: str) -> dict:
    """Запрос к endpoint fastapi binance"""
    try:
        async with session.get(f"/{service}", timeout=15) as exchange_raw_data:
            exchange_data = await exchange_raw_data.json()
    except (asyncio.exceptions.TimeoutError,
            aiohttp.ClientConnectorError,
            aiohttp.ClientOSError,
            OSError) as ex:
        logger.warning(f"Http error fastapi endpoint '{service}' not responding. Exception: {ex}")
        return {}
    if "error" in exchange_data.keys():
        logger.warning(f"{service} endpoint is empty.\n"
                       f"response -> {exchange_data['error']}")
        return {}
    return exchange_data
