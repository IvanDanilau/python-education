from datetime import datetime

import requests

CENTRAL_BANK_RATES_URL = 'https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/'


def get_exchange_rate(date: datetime) -> float:
    response = requests.get(CENTRAL_BANK_RATES_URL, {"date": date}).json()
    if len(list(response)) == 0:
        raise RuntimeError("rate not found")
    for currency in response[0]["currencies"]:
        if currency["code"] == 'USD':
            return currency["rate"]
    raise RuntimeError("rate not found")
