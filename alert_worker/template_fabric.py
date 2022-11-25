from alert_worker.config_for_filter import HIGH_PERCENT
from decimal import Decimal
from aiogram.utils import markdown

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
    minimum, maximum, percent = data["min"], data["max"], data["percent"]
    min_val, volume, min_coin = minimum["buy_price"], minimum["volume"], minimum["exchange"]
    max_val, max_coin = maximum["buy_price"], maximum["exchange"]
    text = f' <i>{currency}</i>:\n' \
           f'Наименьшее: {str(min_val)[:8]}$ - {min_coin}\n' \
           f'Наибольшее: {str(max_val)[:8]}$ - {max_coin}\n' \
           f'Разница: <b>{percent}%</b>\n' \
           '\n' \
           f'Объём торгов: {str(volume)}\n'

    return text
