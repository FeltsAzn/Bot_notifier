from alert_worker.handler_for_volumes import VOLUME_CACHE, dynamic_volumes
from decimal import Decimal, DivisionUndefined
from alert_worker.config_for_filter import START_PERCENT, UP_PERCENT, DOWN_PERCENT
from logger import logger

"""
Файл handler_of_currency.py - главный сортировщик валют.
Вычисляет повышение и понижение значений котировок на биржах.
"""

PERCENT_CACHE = {}


def counter_of_currencies(*args):
    """Обработчик отсеивания не рентабельных данных"""
    coins = [
        "USDT",
        "USDC",
        "BUSD",
        "DAI",
        "BTC"
    ]
    data = {}
    for coin in coins:
        """Получаем максимальное значение биржи по конкретной монете"""
        max_size_exch = max(tuple(map(lambda x: x.get(coin, {}), args)), key=lambda x: len(x))

        for currency, _ in max_size_exch.items():
            """Находим конретные коины из всех бирж"""

            currencies = tuple(map(lambda x: x.get(coin, {}).get(currency, {}), args))
            dynamic_volumes(currency, currencies)
            result: dict = quote_difference(currencies)
            new_percent: float = result["percent"]
            exchange: str = result["min"]["exchange"]

            if new_percent is not None:
                if new_percent >= START_PERCENT:
                    if currency not in PERCENT_CACHE.keys():
                        PERCENT_CACHE[currency] = new_percent

                    if new_percent - PERCENT_CACHE[currency] >= UP_PERCENT:
                        data[currency] = {"price": result,
                                          "state": "up",
                                          "vol": VOLUME_CACHE[(currency, exchange)]
                                          }
                        PERCENT_CACHE[currency] = new_percent

                    elif PERCENT_CACHE[currency] - new_percent >= DOWN_PERCENT:
                        data[currency] = {"price": result,
                                          "state": "down",
                                          "vol": VOLUME_CACHE[(currency, exchange)]
                                          }
                        PERCENT_CACHE[currency] = new_percent
        return data


def quote_difference(*args) -> dict:
    """Высчитывание наименьшего и наибольшего значения, а так же процентный разрыв между ними"""
    max_num: dict = max(*args, key=lambda x: Decimal(x["buy_price"]) if x else -1)
    min_num: dict = min(*args, key=lambda x: Decimal(x["buy_price"]) if x else int(10e8))
    try:
        result = Decimal(f"{str(100 - Decimal(min_num['buy_price']) / Decimal(max_num['buy_price']) * 100)}0000"[:4])
    except DivisionUndefined:
        logger.info(f"Exception DivisionUndefined. Decimal division min num: {Decimal(min_num[0])}"
                    f" | max num: {Decimal(max_num[0])} ")
        result = None
    return {"min": min_num, "max": max_num, "percent": result}
