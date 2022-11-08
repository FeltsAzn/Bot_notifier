from decimal import Decimal
from alert_worker.configs_for_percents import START_PERCENT, INCREASE_PERCENT, DEMOTION_PERCENT

coins_percent_cache = {}


def counter_of_currencies(binance: dict, kucoin: dict, huobi: dict, okx: dict) -> dict[str:tuple[tuple, str]] | dict:
    """Обработчик отсеивания не рентабельных данных"""
    data = {}
    for currency, price in binance.items():
        result: tuple = quote_difference(price, kucoin[currency], huobi[currency], okx[currency])
        new_percent = Decimal(result[2])
        if new_percent >= START_PERCENT:
            # currency_cache
            if currency not in coins_percent_cache.keys():
                coins_percent_cache[currency] = new_percent
            if new_percent - coins_percent_cache[currency] >= INCREASE_PERCENT:
                data[currency] = (result, 'up')
                coins_percent_cache[currency] = new_percent
            elif coins_percent_cache[currency] - new_percent >= DEMOTION_PERCENT:
                data[currency] = (result, "down")
                coins_percent_cache[currency] = new_percent
    return data


def quote_difference(bin_price, kucoin_price, huobi_price, okx_price) -> tuple[list, list, str]:
    """Высчитывание наименьшего и наибольшего значения"""
    max_num: list[str, str] = max(bin_price, kucoin_price, huobi_price, okx_price, key=lambda x: Decimal(x[0]))
    min_num: list[str, str] = min(bin_price, kucoin_price, huobi_price, okx_price, key=lambda x: Decimal(x[0]))
    result = str(100 - Decimal(min_num[0]) / Decimal(max_num[0]) * 100)[:4]
    return min_num, max_num, result
