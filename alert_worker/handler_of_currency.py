from decimal import Decimal
from alert_worker.config_for_filter import START_PERCENT, UP_PERCENT, DOWN_PERCENT

coins_percent_cache = {}


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

        for currency, price in max_size_exch.items():
            """Находим конретные коины из всех бирж"""
            currencies = tuple(map(lambda x: x.get(coin, {}).get(currency, []), args))
            result: tuple[tuple, tuple, Decimal] = quote_difference(currencies)
            new_percent = result[2]

            if new_percent >= START_PERCENT:
                if currency not in coins_percent_cache.keys():
                    coins_percent_cache[currency] = new_percent
                if new_percent - coins_percent_cache[currency] >= UP_PERCENT:
                    data[currency] = (result, 'up')
                    coins_percent_cache[currency] = new_percent
                elif coins_percent_cache[currency] - new_percent >= DOWN_PERCENT:
                    data[currency] = (result, "down")
                    coins_percent_cache[currency] = new_percent
    return data


def quote_difference(*args) -> tuple[tuple, tuple, Decimal]:
    """Высчитывание наименьшего и наибольшего значения, а так же процентный разрыв между ними"""
    max_num: list[str, str] = max(*args, key=lambda x: Decimal(x[0]) if x else 0)
    min_num: list[str, str] = min(*args, key=lambda x: Decimal(x[0]) if x else int(10e8))
    result = Decimal(str(100 - Decimal(min_num[0]) / Decimal(max_num[0]) * 100)[:4])
    max_num: tuple[Decimal, str] = (Decimal(max_num[0]), max_num[1])
    min_num: tuple[Decimal, str] = (Decimal(min_num[0]), min_num[1])
    return min_num, max_num, result
