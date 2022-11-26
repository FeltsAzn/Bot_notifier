from decimal import Decimal
from aiogram.utils import markdown
from alert_worker.config_for_filter import HIGH_PERCENT

"""
Файл template_fabric.py - конфигуратор текстовой информации отсылаемой пользователям
"""


def content_creator(data: dict[str: tuple[dict, str]]) -> list:
    """Функция-фабрика для шаблонов"""
    content = []
    for currency, price in data.items():
        container: dict = price[0]
        state: str = price[1]

        percent = Decimal(container["percent"])

        high_percent = ":bangbang:"
        up_emoji = ":chart_with_upwards_trend:"
        down_emoji = ":chart_with_downwards_trend:"

        text = text_template(currency, container)

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


def text_template(currency: str, data: dict) -> str:
    """Шаблон повышения позиции котировки"""
    min_val = data["min"]["buy_price"]
    volume = data["min"]["volume"]
    min_exchange = data["min"]["exchange"]

    max_val = data["max"]["buy_price"]
    max_exchange = data["max"]["exchange"]

    text = f" <i>{currency}</i>:\n" \
           f"Наименьшее: {str(min_val)[:8]}$ - {min_exchange}\n" \
           f"Наибольшее: {str(max_val)[:8]}$ - {max_exchange}\n" \
           f"Разница: <b>{data['percent']}%</b>\n" \
           "\n" \
           f"Объём торгов: {str(volume)}\n"

    return text
