import os

import bs4
import requests as r
import csv
import logging
import sys

from datetime import datetime

#logging.basicConfig(filename='stock_price.log', level=logging.DEBUG)
logging.StreamHandler(sys.stdout).setLevel(logging.DEBUG)

QUERY_URL_FMT = "http://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes=%s"
ASX_CODES = ['BEN', 'MCY', 'ACX', 'WHC']
NZX_CODES = ['BEN', 'MCY', 'ACX', 'WHC'] #TODO actually use this


def is_price_row(row):
    return 'class' in row.attrs

def get_ASX_stock_prices(codes):
    '''Get stock prices from ASX site (http://www.asx.com.au)'''
    page = r.get(QUERY_URL_FMT % '+'.join(codes)).content.decode()
    soup = bs4.BeautifulSoup(page, 'html.parser')
    rows = list(row for row in soup.find_all('tr') if is_price_row(row))
    return {row.find('th').text.strip(): row.find('td').text.strip() for row in rows}


def get_NZX_stock_prices():
    page = r.get('https://www.nzx.com/markets/nzsx/securities')
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    prices = {}
    for security in soup.find_all('tr')[1:]:
        # TODO refactor to get specific nzx stock
        code, _, price, *_ = [aspect.text.strip('$\n') for aspect in security.find_all('td')]
        prices[code] = price
    return prices


NZX_prices = get_NZX_stock_prices()
ASX_prices = get_ASX_stock_prices(ASX_CODES)
all_prices = dict(NZX_prices, **ASX_prices)

# Write to file for first time
if not os.path.isfile('/home/patrick/Python/stock_scraper/scraper_app/fmt_stock_prices.csv'):
    with open('/home/patrick/Python/stock_scraper/scraper_app/fmt_stock_prices.csv', 'w') as f:
        csvwriter = csv.writer(f)
        # Write stock market
        codes = sorted(all_prices.keys())
        codes_market = []
        for code in codes:
            if code in ASX_CODES:
                codes_market.append('ASX')
            else:
                codes_market.append('NZX')
        csvwriter.writerow(['Stock Exchange', *codes_market])

        # Write codes
        csvwriter.writerow(['Date / Code', *codes])

# Add new values
# TODO Try refactor with numpy
with open('/home/patrick/Python/stock_scraper/scraper_app/fmt_stock_prices.csv', 'a') as f:
    # Write date + price
    # TODO Check if today's prices are already saved
    csvwriter = csv.writer(f)
    today_date = format(datetime.now(), '%m-%d-%Y')
    prices = [price for code, price in sorted(all_prices.items())]
    csvwriter.writerow([today_date, *prices])

