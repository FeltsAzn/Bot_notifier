import time
from decimal import Decimal
from logger import logger

VOLUME_CACHE = {}


def dynamic_volumes(currency: str, exchanges_data: tuple) -> None:
    """Отслеживание динамики объема торгов по котировкам на каждой бирже"""
    for block in exchanges_data:
        if block:
            now_time = time.time()
            exchange = block["exchange"]
            volume = block["volume"]

            if (currency, exchange) not in VOLUME_CACHE.keys():
                cache_creator(currency, exchange, volume)
            timer = VOLUME_CACHE[(currency, exchange)]
            if now_time - timer["5_min"]["time"] > 300:
                cache_updater(now_time, currency, exchange, volume, "5_min")
            if now_time - timer["30_min"]["time"] > 1800:
                cache_updater(now_time, currency, exchange, volume, "30_min")
            if now_time - timer["1_hour"]["time"] > 3600:
                cache_updater(now_time, currency, exchange, volume, "1_hour")
            if now_time - timer["4_hour"]["time"] > 14400:
                cache_updater(now_time, currency, exchange, volume, "4_hour")
            if now_time - timer["1_day"]["time"] > 86400:
                cache_updater(now_time, currency, exchange, volume, "1_day")


def cache_creator(currency: str, exchange: str, volume: str) -> None:
    """Функция для создания кеша, если котировки и биржи нет в кэше"""
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


def cache_updater(
        now_time: float,
        currency_name: str,
        exchange_name: str,
        volume_on_exchange: str,
        time_interval: str
) -> None:
    """Обновление информации по объёму в кэше"""
    old_volume = Decimal(VOLUME_CACHE[(currency_name, exchange_name)][time_interval]["vol"])
    new_volume = Decimal(volume_on_exchange)
    try:
        VOLUME_CACHE[(currency_name, exchange_name)][time_interval]["diff"] = str(100 - old_volume / new_volume * 100)[:5]
    except ValueError:
        logger.info(f"{currency_name} is not for sell on {exchange_name}. Volume is zero")
        VOLUME_CACHE[(currency_name, exchange_name)][time_interval]["diff"] = '0.0'
    VOLUME_CACHE[(currency_name, exchange_name)][time_interval]["vol"] = volume_on_exchange
    VOLUME_CACHE[(currency_name, exchange_name)][time_interval]["time"] = now_time
