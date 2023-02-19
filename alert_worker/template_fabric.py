from decimal import Decimal
from aiogram.utils import markdown
from alert_worker.config_for_filter import HIGH_PERCENT

"""
Файл template_fabric.py - конфигуратор текстовой информации отсылаемой пользователям
"""


def content_creator(data: dict[str: dict]) -> list:
    """Функция-фабрика для шаблонов"""
    content = []
    for currency, info in data.items():
        text_blocks = []
        container: dict = info["price"]
        state: str = info["state"]
        volume: dict[dict] = info["vol"]
        percent = Decimal(container["percent"])

        text_block_price: list = price_percent(currency, container, state, percent)
        text_block_vol: list = volume_percent(container, volume)

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
    high_percent = ":bangbang:"
    up_emoji = ":chart_with_upwards_trend:"
    down_emoji = ":chart_with_downwards_trend:"

    min_val = data["min"]["buy_price"]
    min_exchange = data["min"]["exchange"]

    max_val = data["max"]["buy_price"]
    max_exchange = data["max"]["exchange"]

    text_price = f" <i>{currency}</i>:\n" \
                 f"Наименьшее: {str(min_val)[:8]}$ - {min_exchange}\n" \
                 f"Наибольшее: {str(max_val)[:8]}$ - {max_exchange}\n" \
                 f"Разница: <b>{data['percent']}%</b>\n"
    if state == "up":
        if percent < HIGH_PERCENT:
            text_block = [up_emoji, text_price]
        else:
            text_block = [up_emoji, high_percent, text_price]

    else:
        if percent < HIGH_PERCENT:
            text_block = [down_emoji, text_price]
        else:
            text_block = [down_emoji, high_percent, text_price]
    return text_block


def volume_percent(container: dict, vol: dict) -> list[str]:
    """Сборщик текста для объёмов валют"""

    min_exchange = container["min"]["exchange"]
    up_emoji = ":green_circle:"
    down_emoji = ":red_circle:"
    zero_emoji = ":white_circle:"
    time_intervals = [
        "5_min",
        "30_min",
        "1_hour",
        "4_hour",
        "1_day",
    ]
    volume_segment = [f"Объём торгов на <i>{min_exchange}</i>:\n", ]

    for interval in time_intervals:
        volume_diff: str = vol[interval]["diff"]
        state_of_volume: str = vol[interval]["state"]

        if interval == "5_min":
            volume_segment += template_5m(volume_diff, state_of_volume, up_emoji, down_emoji, zero_emoji)

        elif interval == "30_min":
            volume_segment += template_30m(volume_diff, state_of_volume, up_emoji, down_emoji, zero_emoji)

        elif interval == "1_hour":
            volume_segment += template_1h(volume_diff, state_of_volume, up_emoji, down_emoji, zero_emoji)

        elif interval == "4_hour":
            volume_segment += template_4h(volume_diff, state_of_volume, up_emoji, down_emoji, zero_emoji)

        elif interval == "1_day":
            volume_segment += template_1d(volume_diff, state_of_volume, up_emoji, down_emoji, zero_emoji)
    return volume_segment


def template_5m(
        vol: str,
        state_of_volume: str,
        up_emoji: str,
        down_emoji: str,
        zero_emoji: str
) -> list[str]:
    """Шаблон для 5-ти минутного кэша объёма"""
    if state_of_volume == "up":
        text_segment = [up_emoji, f"<i>5м</i>:    {vol}%\n"]
    elif state_of_volume == "down":
        text_segment = [down_emoji, f"<i>5м</i>:    {vol[1:]}%\n"]
    else:
        text_segment = [zero_emoji, f"<i>5м</i>:    {vol}%\n"]
    return text_segment


def template_30m(
        vol: str,
        state_of_volume: str,
        up_emoji: str,
        down_emoji: str,
        zero_emoji: str
) -> list[str]:
    """Шаблон для 30-ти минутного кэша объёма"""
    if state_of_volume == "up":
        text_segment = [up_emoji, f"<i>30м</i>:  {vol}%\n"]
    elif state_of_volume == "down":
        text_segment = [down_emoji, f"<i>30м</i>:  {vol[1:]}%\n"]
    else:
        text_segment = [zero_emoji, f"<i>30м</i>:  {vol}%\n"]
    return text_segment


def template_1h(
        vol: str,
        state_of_volume: str,
        up_emoji: str,
        down_emoji: str,
        zero_emoji: str
) -> list[str]:
    """Шаблон для часового кэша объёма"""
    if state_of_volume == "up":
        text_segment = [up_emoji, f"<i>1ч</i>:     {vol}%\n"]
    elif state_of_volume == "down":
        text_segment = [down_emoji, f"<i>1ч</i>:     {vol[1:]}%\n"]
    else:
        text_segment = [zero_emoji, f"<i>1ч</i>:     {vol}%\n"]
    return text_segment


def template_4h(
        vol: str,
        state_of_volume: str,
        up_emoji: str,
        down_emoji: str,
        zero_emoji: str
) -> list[str]:
    """Шаблон для 4-х часового кэша объёма"""
    if state_of_volume == "up":
        text_segment = [up_emoji, f"<i>4ч</i>:     {vol}%\n"]
    elif state_of_volume == "down":
        text_segment = [down_emoji, f"<i>4ч</i>:     {vol[1:]}%\n"]
    else:
        text_segment = [zero_emoji, f"<i>4ч</i>:     {vol}%\n"]
    return text_segment


def template_1d(
        vol: str,
        state_of_volume: str,
        up_emoji: str,
        down_emoji: str,
        zero_emoji: str
) -> list[str]:
    """Шаблон для дневного кэша объёма"""
    if state_of_volume == "up":
        text_segment = [up_emoji, f"<i>день</i>: {vol}%\n"]
    elif state_of_volume == "down":
        text_segment = [down_emoji, f"<i>день</i>: {vol[1:]}%\n"]
    else:
        text_segment = [zero_emoji, f"<i>день</i>: {vol}%\n\n"]
    return text_segment
