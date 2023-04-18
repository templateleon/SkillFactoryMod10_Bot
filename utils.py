import json
import requests
from config import keys, APY_KEY


class ConvertionException(Exception):
    pass


class CurrencyConverter:

    @staticmethod
    def convert(quote, base, amount):

        error_text = 'Введите валюты заново или выберите \nМеню --> Кнопки'

        if quote == base:
            raise ConvertionException(
                f'Нельзя конвертировать {quote} в {quote} {error_text}')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError as exc:
            raise ConvertionException(
                f'Не удалось обработать валюту {quote}  {error_text}') from exc

        try:
            base_ticker = keys[base.lower()]
        except KeyError as exc:
            raise ConvertionException(
                f'Не удалось обработать валюту {base} {error_text}') from exc

        try:
            amount = float(amount)
        except ValueError as exc:
            raise ConvertionException(
                f'Не удалось обработать количество {amount}  {error_text}') from exc

        url = (
            f"https://api.apilayer.com/exchangerates_data/convert?to={quote_ticker}&from={base_ticker}&amount={amount}")
        payload = {}
        headers = {"apikey": APY_KEY}
        r = requests.request("GET", url, headers=headers, data=payload, timeout=20)
        result = json.loads(r.content)
        convert_price = round(result['result'], 2)
        # print(result)
        message = f'Покупка {amount} {base_ticker} обойдется вам {convert_price} {quote_ticker} \n\n Надо повторить? \n{error_text}'
        return message
