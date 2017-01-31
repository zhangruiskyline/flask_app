import csv
import requests
from yahoo_finance import Share
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urlencode
from collections import deque
from threading import Thread
from time import time, sleep
from datetime import datetime
import csv
import codecs
from threading import Thread, current_thread

# In memory RRDB
stock_values = deque(maxlen=1000)
threadErrors = []



def get_nasdaq_100_data():
    nasdaq_100_URL = "http://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx?render=download"
    r = requests.get(nasdaq_100_URL)
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

def gen_url(stock):
    url = 'http://download.finance.yahoo.com/d/quotes.csv'
    query = {
        's': stock,
        'f': 'nsl1op',
        'e': '.csv',
    }
    return '%s?%s' % (url, urlencode(query))


def poll_data(stock_symbol):
    url = gen_url(stock_symbol)
    decoder = codecs.getreader('utf-8')
    while True:
        fo = decoder(urlopen(url))
        for row in csv.reader(fo):
            # "Google Inc.","GOOG",547.04,543.00,540.77
            price = float(row[2])
            break
        stock_values.append((time(), price))
        sleep(3)

def stock_stream_thread(stock_symbol):
    try:
        thr = Thread(target=poll_data, args=(stock_symbol,))
        thr.daemon = True
        thr.start()
    except Exception, e:
        threadErrors.append([repr(e), current_thread.name])  # append a list of info
        raise  # re-raise the exception or use sys.exit(1) to let the thread die and free resources
