from alert_worker.configs_for_percents import HIGH_PERCENT
from decimal import Decimal
from aiogram.utils import markdown


def content_creator(data: dict[str:tuple[tuple, str]]) -> list:
    """Функция-фабрика для шаблонов"""
    content = []
    for currency, price in data.items():
        data, state = price
        percent = Decimal(data[2])

        high_percent = ":bangbang:"
        up_emoji = ":chart_with_upwards_trend:"
        down_emoji = ":chart_with_downwards_trend:"

        text = text_template(currency, data)

        if state == "up":
            if percent <= HIGH_PERCENT:
                content.append(markdown.text(up_emoji, text))
            else:
                content.append(markdown.text(up_emoji, high_percent, text))
        elif state == "down":
            if percent <= HIGH_PERCENT:
                content.append(markdown.text(down_emoji, text))
            else:
                content.append(markdown.text(down_emoji, high_percent, text))

    return content


def text_template(currency: str, data: tuple[list, list, str]) -> str:
    """Шаблон повышения позиции котировки"""
    minimum, maximum, percent = data
    min_val, min_coin = minimum
    max_val, max_coin = maximum
    text = f' <i>{currency}</i>:\n' \
           f'Наименьшее: {str(min_val)[:8]}$ - {min_coin}\n' \
           f'Наибольшее: {str(max_val)[:8]}$ - {max_coin}\n' \
           f'Разница: <b>{percent}%</b>\n\n'
    return text
