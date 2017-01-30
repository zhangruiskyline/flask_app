import csv
import requests
from yahoo_finance import Share


URL = "http://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx?render=download"


def get_nasdaq_100_data():
    r = requests.get(URL)
    data = r.text
    RESULTS = {'children': []}
    for line in csv.DictReader(data.splitlines(), skipinitialspace=True):
        if float(line['Nasdaq100_points']) > .01:
            RESULTS['children'].append({
                'name': line['Name'],
                'symbol': line['Symbol'],
                'price': line['lastsale'],
                'net_change': line['netchange'],
                'percent_change': line['pctchange'],
                'volume': line['share_volume'],
                'value': line['Nasdaq100_points']
            })
    return RESULTS

def yahoo_get_all_data(symbol):
    RESULTS = []
    company = Share(symbol)
    stock_price = company.get_price()
    stock_vol = company.get_volume()
    stock_cap = company.get_market_cap()
    RESULTS.append({
        'symbol': symbol,
        'price': stock_price,
        'vol': stock_vol,
        'cap': stock_cap,
    })

    return RESULTS
