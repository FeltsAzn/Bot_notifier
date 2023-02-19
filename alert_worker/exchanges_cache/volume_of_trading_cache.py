import time
from logger import logger
from loader import VOLUME_CONNECTION

"""
volume_of_trading_cache.py file - Cache updater.
Is uses for tracking a volumes of quotes on exchanges and update information about volumes.
Using redis to saving a values
"""

class VolumeCache:
    __CACHE_CONN = VOLUME_CONNECTION

    def __init__(self, currency: str, exchanges_data: tuple):
        self.currency = currency
        self.exchanges_data = exchanges_data


    def dynamic_volumes(self) -> None:
        """Отслеживание динамики объема торгов по котировкам на каждой бирже"""
        with self.__CACHE_CONN as cache:
            for data_block in self.exchanges_data:
                if data_block:
                    self.__difference_between_data(data_block, cache)

    def __difference_between_data(self, block, cache) -> None:
        now_time = time.time()
        exchange = block["exchange"]
        volume = block["volume"]
        key_of_currency = f"{self.currency}|{exchange}"
        if not cache.check_key_in_redis(key_of_currency):
            template = self.__create_template(volume)
            cache.create_key_and_value(key_of_currency, template)

        timer: dict = cache.get_value(key_of_currency)
        if now_time - timer["5_min"]["time"] > 300:
            timer["5_min"] = self.__update_time_and_difference(timer["5_min"], now_time, exchange, volume)
            cache.update_exist_key(key_of_currency, timer)

        if now_time - timer["30_min"]["time"] > 1800:
            timer["30_min"] = self.__update_time_and_difference(timer["30_min"], now_time, exchange, volume)
            cache.update_exist_key(key_of_currency, timer)

        if now_time - timer["1_hour"]["time"] > 3600:
            timer["1_hour"] = self.__update_time_and_difference(timer["1_hour"], now_time, exchange, volume)
            cache.update_exist_key(key_of_currency, timer)

        if now_time - timer["4_hour"]["time"] > 14400:
            timer["4_hour"] = self.__update_time_and_difference(timer["4_hour"], now_time, exchange, volume)
            cache.update_exist_key(key_of_currency, timer)

        if now_time - timer["1_day"]["time"] > 86400:
            timer["1_day"] = self.__update_time_and_difference(timer["1_day"], now_time, exchange, volume)
            cache.update_exist_key(key_of_currency, timer)

    def __update_time_and_difference(
            self,
            data_block: dict,
            now_time: float,
            exchange_name: str,
            volume_on_exchange: str,
    ) -> dict:
        """Update information about a cache of volumes """
        old_volume = float(data_block["vol"])
        new_volume = float(volume_on_exchange)
        try:
            volume_difference = new_volume / old_volume * 100 - 100
            data_block["diff"] = str(volume_difference)[:5]
            if volume_difference > 0:
                data_block["state"] = "up"
            elif volume_difference < 0:
                data_block["state"] = "down"
            else:
                data_block["state"] = "none"
        except ZeroDivisionError:
            if new_volume != 0:
                data_block["diff"] = str(100)
                data_block["state"] = "up"
            else:
                logger.info(f"Currency {self.currency} is not for sell on {exchange_name}. Volume is zero\n"
                            f"Old volume = {old_volume}, new volume {new_volume}")
                data_block["diff"] = str(0)
                data_block["state"] = "none"

        data_block["vol"] = volume_on_exchange
        data_block["time"] = now_time
        return data_block

    @staticmethod
    def __create_template(volume: str) -> dict:
        """Func for creating the volume template"""
        time_start = time.time()
        template = {
            "5_min": {
                "time": time_start,
                "vol": volume,
                "diff": 0.00,
                "state": "none"
            },
            "30_min": {
                "time": time_start,
                "vol": volume,
                "diff": 0.00,
                "state": "none"
            },
            "1_hour": {
                "time": time_start,
                "vol": volume,
                "diff": 0.00,
                "state": "none"
            },
            "4_hour": {
                "time": time_start,
                "vol": volume,
                "diff": 0.00,
                "state": "none"
            },
            "1_day": {
                "time": time_start,
                "vol": volume,
                "diff": 0.00,
                "state": "none"
            }
        }
        return template

    def get_currency_volume(self, currency: str) -> dict:
        with self.__CACHE_CONN as cache:
            volume = cache.get_value(currency)
        if volume is None:
            return {}
        return volume



