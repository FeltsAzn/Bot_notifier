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
        container: dict = info["price"]
        state: str = info["state"]
        volume: dict[dict] = info["vol"]

        percent = Decimal(container["percent"])

        high_percent = ":bangbang:"
        up_emoji = ":chart_with_upwards_trend:"
        down_emoji = ":chart_with_downwards_trend:"

        text = text_template(currency, container, volume)

        if state == "up":
            if percent < HIGH_PERCENT:
                content.append(markdown.text(up_emoji, text))
            else:
                content.append(markdown.text(up_emoji, high_percent, text))

        elif state == "down":
            if percent < HIGH_PERCENT:
                content.append(markdown.text(down_emoji, text))
            else:
                content.append(markdown.text(down_emoji, high_percent, text))

    return content


def text_template(currency: str, data: dict, vol: dict) -> str:
    """Шаблон повышения позиции котировки"""
    min_val = data["min"]["buy_price"]
    min_exchange = data["min"]["exchange"]

    max_val = data["max"]["buy_price"]
    max_exchange = data["max"]["exchange"]

    text = f" <i>{currency}</i>:\n" \
           f"Наименьшее: {str(min_val)[:8]}$ - {min_exchange}\n" \
           f"Наибольшее: {str(max_val)[:8]}$ - {max_exchange}\n" \
           f"Разница: <b>{data['percent']}%</b>\n" \
           "\n" \
           f"Объём торгов на {min_exchange}:\n" \
           f"5m {vol['5_min']['diff']}% 30m {vol['30_min']['diff']}% 1h {vol['1_hour']['diff']}%" \
           f" 4h {vol['4_hour']['diff']}% 1d {vol['1_day']['diff']}%\n"
    return text
