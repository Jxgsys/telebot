import json
import requests
from config import api_key, keys

class ConvertionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Введена одна валюта {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://freecurrencyapi.net/api/v2/latest?apikey={api_key}&base_currency={quote_ticker}')
        valuta2 = json.loads(r.content)['data'].get(keys[base])
        total_base = float(valuta2) * float(amount)
        return total_base