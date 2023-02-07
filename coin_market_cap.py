'''
Pre-requisite: 
- Create a file "keys.py" with your content:
"API_KEY = XXa303XX-XX35-XX1e-9204-XXb54a01cdXX"

- Class to get BTC data from CoinMarketCap API with developer keys.
Specific data to be parsed is volume and change in past 1h, 24h, 7d

Later, this is used to make decision for 3cqs Bot pause during BTC dips
and Bot resume on BTC recovery signs

- API Documentation:
https://coinmarketcap.com/api/documentation/v1/#section/Endpoint-Overview
'''

import keys
import json

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

class CoinMarketCap:

  def __init__(self, API_KEY):
    self.base_url = 'https://sandbox-api.coinmarketcap.com'
    self.headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': API_KEY,
    }
    self.session = Session()
    self.session.headers.update(self.headers)
    
    # self.parameters = {
    #   'start':'1',
    #   'limit':'5000',
    #   'convert':'USD'
    # }


  def get_all_latest(self):
    url = self.base_url + '/v1/cryptocurrency/listings/latest'
    r = self.session.get(url)
    data = json.loads(r.text)
    return data


  def get_by_symbol(self, symbol='BTC', currency='USD'):
    url = self.base_url + '/v1/cryptocurrency/quotes/latest'
    parameters = {'symbol': symbol}
    r = self.session.get(url, params=parameters)
    data = json.loads(r.text)
    return data


  def get_volume(self, symbol='BTC', currency='USD'):
    data = self.get_by_symbol(symbol, currency)
    volume = data['data'][symbol]['quote'][currency]
    return {
            volume['last_updated'], 
            volume['percent_change_1h'], 
            volume['volume_24h'], 
            volume['percent_change_24h']
           }
    '''
      "USD": {
        "price": 0.8435165816653007,
        "volume_24h": 0.030134655524648446,
        "volume_change_24h": 0.4410692009547936,
        "percent_change_1h": 0.4996866028309588,
        "percent_change_24h": 0.9083645229839803,
        "percent_change_7d": 0.18183716848818055,
        "percent_change_30d": 0.5791838552167197,
        "market_cap": 0.4537036190380592,
        "market_cap_dominance": 3571,
        "fully_diluted_market_cap": 0.26881926302516157,
        "last_updated": "2023-02-07T13:57:37.443Z"
    }
    '''


def main():
  if __name__ == "__main__":
    cmc = CoinMarketCap(keys.API_KEY)

    try:
      data = cmc.get_volume('BTC')
      print(json.dumps(data, indent=4))
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

main()