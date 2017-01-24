import bs4
import requests
import pprint
import re
import csv
import logging
import sys
from datetime import date

PRICE_RE = re.compile('^\d+\.\d+$')
#logging.basicConfig(filename='stock_price.log', level=logging.DEBUG)
logging.StreamHandler(sys.stdout).setLevel(logging.DEBUG)

max_rows = 30
def get_codes():
    symbols = []
    for start in range(0, max_rows, 30):
        page = requests.get('https://www.google.com/finance?q=NZE%3A&restype=company&noIL=1&num=30&start=' + str(start)).content
        soup = bs4.BeautifulSoup(page, 'html.parser')
        td_texts = [tag.text for tag in soup.find_all(name='td', attrs={'class': 'symbol'})]
        symbols.extend(td_text.strip().split()[0] for td_text in td_texts)
    logging.info('Found the following codes: ' + str(sorted(symbols)))
    return set(symbols)

codes = get_codes() # TODO get from search page
with open('stock_prices.csv', 'a') as f:
    csvwriter = csv.writer(f)
    for code in codes:
        page = requests.get('https://www.google.com/finance?q=NZE%3A' + code)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        try:
            stock_price = float(soup.find(name='span', text=PRICE_RE).text)
        except (ValueError, AttributeError):
            logging.warning('Could not retrieve stock price from %s' % code)
        else:
            logging.info('Retrieved stock price for %s: %f' % (code, stock_price,))
            logging.info('Writing to' + f.name)
            csvwriter.writerow([date.today(), code, stock_price])
