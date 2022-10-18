import re

import requests

from redis_handler import recording_dollar_value, check_dollar_value


def get_dollar_value() -> float:
    """Получаем значения доллара из redis, если значения нет, парсим сайт,
    для получения значения и записываем его в redis.

    Return:
        float: значение доллара.
    """
    dollar_value_cache = check_dollar_value()
    if dollar_value_cache is None:
        dollar_html = requests.get("https://www.banki.ru/products/currency/usd/")
        dollar_value = re.search(
            r'<div class="currency-table__large-text">(\d+.\d+)', dollar_html.text
        ).group(1)
        dollar_value = dollar_value.replace(",", ".")
        recording_dollar_value(dollar_value)
    else:
        dollar_value = dollar_value_cache.decode("utf-8", "replace")

    return float(dollar_value)
