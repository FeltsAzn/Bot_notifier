import decimal
import json
from datetime import datetime
import time
from decimal import Decimal, DivisionUndefined
from alert_worker.config_for_filter import START_PERCENT, UP_PERCENT, DOWN_PERCENT
from logger import logger

"""
Файл handler_of_currency.py - главный сортировщик валют.
Вычисляет повышение и понижение значений котировок на биржах.
"""

PERCENT_CACHE = {}
VOLUME_CACHE = {}


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


def dynamic_volumes(currency: str, exchanges_data: tuple) -> None:
    for block in exchanges_data:
        if block:
            now_time = time.time()
            exchange = block["exchange"]
            volume = block["volume"]

            ### 5m, 30m, 1h, 4h,
            if (currency, exchange) not in VOLUME_CACHE.keys():
                time_start = time.time()
                VOLUME_CACHE[(currency, exchange)] = {
                    "5_min": {
                        "time": time_start,
                        "vol": volume,
                        "diff": 0.00
                    },
                    "30_min": {
                        "time": time_start,
                        "vol": volume,
                        "diff": 0.00
                    },
                    "1_hour": {
                        "time": time_start,
                        "vol": volume,
                        "diff": 0.00
                    },
                    "4_hour": {
                        "time": time_start,
                        "vol": volume,
                        "diff": 0.00
                    },
                    "1_day": {
                        "time": time_start,
                        "vol": volume,
                        "diff": 0.00
                    }
                }
            timer = VOLUME_CACHE[(currency, exchange)]
            try:

                if now_time - timer["5_min"]["time"] > 300:
                    VOLUME_CACHE[(currency, exchange)]["5_min"]["diff"] = (
                            100 - Decimal(timer["5_min"]["vol"]) / Decimal(volume) * 100)
                    VOLUME_CACHE[(currency, exchange)]["5_min"]["vol"] = volume
                    VOLUME_CACHE[(currency, exchange)]["5_min"]["time"] = now_time

                if now_time - timer["30_min"]["time"] > 1800:
                    VOLUME_CACHE[(currency, exchange)]["30_min"]["diff"] = (
                            100 - Decimal(timer["30_min"]["vol"]) / Decimal(volume) * 100)
                    VOLUME_CACHE[(currency, exchange)]["30_min"]["vol"] = volume
                    VOLUME_CACHE[(currency, exchange)]["30_min"]["time"] = now_time

                if now_time - timer["1_hour"]["time"] > 3600:
                    VOLUME_CACHE[(currency, exchange)]["1_hour"]["diff"] = (
                            100 - Decimal(timer["1_hour"]["vol"]) / Decimal(volume) * 100)
                    VOLUME_CACHE[(currency, exchange)]["1_hour"]["vol"] = volume
                    VOLUME_CACHE[(currency, exchange)]["1_hour"]["time"] = now_time

                if now_time - timer["4_hour"]["time"] > 14400:
                    VOLUME_CACHE[(currency, exchange)]["4_hour"]["diff"] = (
                            100 - Decimal(timer["4_hour"]["vol"]) / Decimal(volume) * 100)
                    VOLUME_CACHE[(currency, exchange)]["4_hour"]["vol"] = volume
                    VOLUME_CACHE[(currency, exchange)]["4_hour"]["time"] = now_time

                if now_time - timer["1_day"]["time"] > 86400:
                    VOLUME_CACHE[(currency, exchange)]["1_day"]["diff"] = (
                            100 - Decimal(timer["1_day"]["vol"]) / Decimal(volume) * 100)
                    VOLUME_CACHE[(currency, exchange)]["1_day"]["vol"] = volume
                    VOLUME_CACHE[(currency, exchange)]["1_day"]["time"] = now_time
            except decimal.InvalidOperation as ex:
                logger.exception(f'{ex} data: {timer}, volume:{volume}')


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
