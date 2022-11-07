import aiohttp


async def binance_info(session: aiohttp.ClientSession) -> dict:
    """Запрос к endpoint fastapi binance"""
    async with session.get('/binance') as binance:
        binance = await binance.json()
    return binance


async def kucoin_info(session: aiohttp.ClientSession) -> dict:
    """Запрос к endpoint fastapi kucoin"""
    async with session.get('/kucoin') as kucoin:
        kucoin = await kucoin.json()
    return kucoin


async def huobi_info(session: aiohttp.ClientSession) -> dict:
    """Запрос к endpoint fastapi huobi"""
    async with session.get('/huobi') as huobi:
        huobi = await huobi.json()
    return huobi


async def okx_info(session: aiohttp.ClientSession) -> dict:
    """Запрос к endpoint fastapi okx"""
    async with session.get('/okx') as okx:
        okx = await okx.json()
    return okx