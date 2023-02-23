from alert_worker.exchanges_cache.volume_of_trading_cache import VolumeCache
from decimal import Decimal, DivisionUndefined
from alert_worker.config_for_filter import START_PERCENT, UP_PERCENT, DOWN_PERCENT
from logger import logger
# from loader import CURRENCY_CONNECTION
from cache.redis_logic import RedisCache

"""
quotes_of_currency_cache.py File - The main currency sorter.
Is computes upgrade and downgrade a values of quotes on exchanges.
Using redis to saving a values.
"""


class CurrencyCache:
    CURRENCY_CONNECTION = None
    __CACHE_CONN = CURRENCY_CONNECTION

    def counter_of_currencies(self, *args) -> dict:
        """Обработчик отсеивания не рентабельных данных"""
        coins = [
            "USDT",
            "USDC",
            "BUSD",
            "DAI",
            "BTC"
        ]
        collection_data_for_sending = {}

        with self.__CACHE_CONN as cache:
            for coin in coins:
                """Получаем максимальное значение биржи (количества коинов) по конкретной монете"""
                max_size_of_exchange = max(tuple(map(lambda x: x.get(coin, {}), args)), key=lambda x: len(x))

                for currency, _ in max_size_of_exchange.items():
                    """Находим конкретные коины из всех бирж"""

                    currency_on_exchanges = tuple(map(lambda x: x.get(coin, {}).get(currency, {}), args))
                    volume_of_currency = VolumeCache(currency, currency_on_exchanges)
                    volume_of_currency.dynamic_volumes()
                    result_of_quote_difference = self.__quote_difference(*currency_on_exchanges)
                    collection_data_for_sending = self.__filling_data_to_send(result_of_quote_difference,
                                                       cache,
                                                       currency,
                                                       volume_of_currency,
                                                       collection_data_for_sending)
            return collection_data_for_sending

    @staticmethod
    def __filling_data_to_send(result: dict, cache: RedisCache, currency: str, volume: VolumeCache, data: dict):
        new_percent: float = result["percent"]
        exchange_name: str = result["min"]["exchange"]

        if new_percent is not None:
            currency_volume: dict = volume.get_currency_volume(f"{currency}|{exchange_name}")
            if new_percent >= START_PERCENT and float(currency_volume["5_min"]["vol"]):

                if not cache.check_key_in_redis(currency):
                    cache.create_key_and_value(currency, new_percent)

                if new_percent - cache.get_value(currency) >= UP_PERCENT:
                    data[currency] = {
                        "price": result,
                        "state": "up",
                        "vol": currency_volume
                    }
                    cache.update_exist_key(currency, new_percent)

                elif cache.get_value(currency) - new_percent >= DOWN_PERCENT:
                    data[currency] = {
                        "price": result,
                        "state": "down",
                        "vol": currency_volume
                    }
                    cache.update_exist_key(currency, new_percent)
        return data

    @staticmethod
    def __quote_difference(*args) -> dict:
        """Calculation max and min value, and also percentage gap between them"""
        max_num: dict = max(*args, key=lambda x: Decimal(x["buy_price"]) if x else -1)
        min_num: dict = min(*args, key=lambda x: Decimal(x["buy_price"]) if x else int(10e8))
        try:
            percent = float(f"{str(100 - Decimal(min_num['buy_price']) / Decimal(max_num['buy_price']) * 100)}0000"[:4])
        except DivisionUndefined:
            logger.info(f"Exception DivisionUndefined. Decimal division min num: {Decimal(min_num[0])}"
                        f" | max num: {Decimal(max_num[0])} ")
            percent = None
        return {"min": min_num, "max": max_num, "percent": percent}
