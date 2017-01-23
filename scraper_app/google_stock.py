import bs4
import requests
import pprint
import re
import csv
import logging
from datetime import date

PRICE_RE = re.compile('^\d+\.\d+$')
logging.basicConfig(filename='stock_price.log', level=logging.DEBUG)
codes = ['ATM','AFC','AFT','A01C','WIN'] # TODO get from search page
with open('stock_prices.csv', 'a') as f:
    csvwriter = csv.writer(f)
    for code in codes:
        page = requests.get('https://www.google.com/finance?q=NZE%3A' + code)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        try:
            stock_price = float(soup.find(name='span', text=PRICE_RE).text)
        except ValueError:
            logging.warning('Could not retrieve stock price from %s' % code)
        logging.info('Retrieved stock price for %s: %f' % (code, stock_price,))
        csvwriter.writerow([date.today(), code, stock_price])
