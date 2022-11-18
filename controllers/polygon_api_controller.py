import requests
import json
import os
from datetime import date, timedelta
from abc import ABC, abstractmethod


def token_value():
    r = requests.get(os.getenv('POLYGON_ENDPOINT') + 'v1' +
                     "/open-close/crypto/MATIC/USD/" +
                     str(date.today()) +
                     f"?apiKey={os.getenv('POLYGON_API_KEY')}")
    j = json.loads(r.text)
    return j['close']


def value_over_time(days):
    r = requests.get(os.getenv('POLYGON_ENDPOINT') + 'v2' +
                     '/aggs/ticker/X:MATICUSD/range/1/day/' +
                     str(date.today() - timedelta(days=days)) + '/' + str(date.today()) +
                     '?adjusted=true&sort=asc&limit=365&' +
                     f"apiKey={os.getenv('POLYGON_API_KEY')}")
    j = json.loads(r.text)
    values = [x['o'] for x in j['results']]
    return {'values': values, 'min': min(values), 'max': max(values)}
