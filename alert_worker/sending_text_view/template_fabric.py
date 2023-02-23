from decimal import Decimal
from aiogram.utils import markdown
from alert_worker.config_for_filter import HIGH_PERCENT
from alert_worker.sending_text_view.text_configs import *
"""
Файл template_fabric.py - конфигуратор текстовой информации отсылаемой пользователям
"""


def content_creator(data: dict[str: dict]) -> list:
    """Функция-фабрика для шаблонов"""
    content = []
    for currency, info in data.items():
        text_blocks = []

        container: dict = info["price"]
        min_exchange_name: str = container["min"]["exchange"]
        state_of_currency: str = info["state"]
        volume: dict[dict] = info["vol"]
        percent = Decimal(container["percent"])

        text_block_price: list = price_percent(currency, container, state_of_currency, percent)
        text_block_vol: list = volume_percent(min_exchange_name, volume)

        text_blocks += text_block_price
        text_blocks += text_block_vol
        content.append(markdown.text(*text_blocks))
    return content


def price_percent(
        currency: str,
        data: dict,
        state: str,
        percent: Decimal
) -> list[str]:
    """Сборщик шаблона для информации по котировкам"""
    min_val = data["min"]["buy_price"]
    min_exchange = data["min"]["exchange"]

    max_val = data["max"]["buy_price"]
    max_exchange = data["max"]["exchange"]

    text_price = f" <b><i>{currency}</i></b>:\n" \
                 f"<i>min:</i> {str(min_val)[:10]}$ - {min_exchange}\n" \
                 f"<i>max:</i> {str(max_val)[:10]}$ - {max_exchange}\n" \
                 f"<i>diff:</i> <b>{data['percent']}%</b>\n\n"
    match state:
        case "up":
            if percent < HIGH_PERCENT:
                text_block = [up_emoji_currency, text_price]
            else:
                text_block = [up_emoji_currency, high_percent_header, text_price]
        case _:
            if percent < HIGH_PERCENT:
                text_block = [down_emoji_currency, text_price]
            else:
                text_block = [down_emoji_currency, high_percent_header, text_price]
    return text_block


def volume_percent(min_exchange_name: str, vol: dict) -> list[str]:
    """Сборщик текста для объёмов валют"""

    volume_segment = [f"<i>Volume of trading on <b>{min_exchange_name}</b>:</i>\n", ]

    for interval in time_intervals:
        volume_diff  = abs(float(vol[interval]["diff"]))
        state_of_volume: str = vol[interval]["state"]

        volume_segment += create_volume_data_block(interval, volume_diff, state_of_volume)

    return volume_segment


def create_volume_data_block(time_diff: str, volume_percent: float, state_of_volume: str) -> list[str]:
    """Шаблон для 5-ти минутного кэша объёма"""
    text_templates = {
        "5_min": [f"<i>5m</i>:    {volume_percent}%\n"],
        "30_min": [f"<i>30m</i>:  {volume_percent}%\n"],
        "1_hour": [f"<i>1h</i>:      {volume_percent}%\n"],
        "4_hour": [f"<i>4h</i>:      {volume_percent}%\n"],
        "1_day": [f"<i>day</i>:    {volume_percent}%\n\n\n"]
    }

    text_segment = text_templates[time_diff]
    match state_of_volume:
        case "up":
            text_segment.insert(0, up_emoji_vol)
        case "down":
            text_segment.insert(0, down_emoji_vol)
        case _:
            text_segment.insert(0, zero_emoji_vol)
    return text_segment
