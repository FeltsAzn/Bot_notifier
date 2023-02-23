import os
import aiohttp
from logger import logger
import asyncio
from aiohttp.client_exceptions import ContentTypeError
"""
Файл http_req.py - запросы к endpoint'ам приложения на FastAPI
"""
TEXT_CREATOR_URL = os.getenv("TEXT_GENERATOR")
EXCHANGES_DATA_URL = os.getenv("EXCHANGES_DATA_COLLECTOR")

async def exchanges_data_collector() -> tuple:
    """Collector of data on different exchanges"""
    async with aiohttp.ClientSession(EXCHANGES_DATA_URL) as session:
        list_of_exchanges = [
            "binance",
            "kucoin",
            "huobi",
            "okx"
        ]
        tasks = []
        for exchange in list_of_exchanges:
            request = send_request(session, exchange)
            tasks.append(request)
        all_data = await asyncio.gather(*tasks)
    return all_data


async def send_request(session: aiohttp.ClientSession, service: str) -> dict:
    try:
        async with session.get(f"/{service}", timeout=15) as raw_data:
            convert_data = await raw_data.json()
    except (asyncio.exceptions.TimeoutError,
            aiohttp.ClientConnectorError,
            aiohttp.ClientOSError,
            ContentTypeError,
            OSError) as ex:
        logger.warning(f"Http error exchanges endpoint '{service}' not responding. Exception: {ex}")
        return {}
    if "error" in convert_data.keys():
        logger.warning(f"{service} endpoint is empty.\n"
                       f"response -> {convert_data['error']}")
        return {}
    return convert_data


async def give_finished_text(*raw_data) -> list:
    async with aiohttp.ClientSession(TEXT_CREATOR_URL) as session:
        converted_data = {"data": [*raw_data]}
        try:
            async with session.post(f"/get_text", json=converted_data, timeout=5) as response:
                text_block = await response.json()
        except (asyncio.exceptions.TimeoutError,
                aiohttp.ClientConnectorError,
                aiohttp.ClientOSError,
                ContentTypeError,
                OSError) as ex:
            logger.warning(f"Http error text creator service endpoint not responding. Exception: {ex}")
            return []
        if "error" in text_block.keys():
            logger.warning(f"Error in text creator.\n"
                           f"response -> {text_block['error']}")
            return []
        return text_block["data"]