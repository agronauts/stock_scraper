import bs4
import requests
import pprint
import re

PRICE_RE = re.compile('^\d+\.\d+$')
codes = ['ATM','AFC','AFT','A01C','WIN'] # TODO get from search page
for code in codes:
    page = requests.get('https://www.google.com/finance?q=NZE%3A' + code)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    # TODO verify numbers
    stock_price = float(soup.find(name='span', text=PRICE_RE).text)
    pprint.pprint(stock_price)
    # TODO write results to file
    # TODO log errors in seperate file
