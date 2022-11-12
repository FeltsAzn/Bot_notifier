import aiohttp
from logs.logger import logger


async def binance_info(session: aiohttp.ClientSession) -> dict:
    """Запрос к endpoint fastapi binance"""
    async with session.get('/binance') as binance:
        binance = await binance.json()
    if "error" in binance.keys():
        logger.warning(f"Binance endpoint is empty.\n"
                       f"response -> {binance['error']}")
        return {}
    return binance


async def kucoin_info(session: aiohttp.ClientSession) -> dict:
    """Запрос к endpoint fastapi kucoin"""
    async with session.get('/kucoin') as kucoin:
        kucoin = await kucoin.json()
    if "error" in kucoin.keys():
        logger.warning(f"Binance endpoint is empty.\n"
                       f"response -> {kucoin['error']}")
        return {}
    return kucoin


async def huobi_info(session: aiohttp.ClientSession) -> dict:
    """Запрос к endpoint fastapi huobi"""
    async with session.get('/huobi') as huobi:
        huobi = await huobi.json()
    if "error" in huobi.keys():
        logger.warning(f"Binance endpoint is empty.\n"
                       f"response -> {huobi['error']}")
        return {}
    return huobi


async def okx_info(session: aiohttp.ClientSession) -> dict:
    """Запрос к endpoint fastapi okx"""
    async with session.get('/okx') as okx:
        okx = await okx.json()
    if "error" in okx.keys():
        logger.warning(f"Binance endpoint is empty.\n"
                       f"response -> {okx['error']}")
        return {}
    return okx