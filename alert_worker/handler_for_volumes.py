import decimal
import time
from decimal import Decimal, DivisionUndefined
from logger import logger


VOLUME_CACHE = {}


def dynamic_volumes(currency: str, exchanges_data: tuple) -> None:
    for block in exchanges_data:
        if block:
            now_time = time.time()
            exchange = block["exchange"]
            volume = block["volume"]
            # with open("file.json", 'a') as file:
            #     json.dump(block, file, indent=4)
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
                print('error with decimal operation')