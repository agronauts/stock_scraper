#!/usr/bin/python3

import os

import bs4
import requests as r
import csv
import logging
import sys

from datetime import datetime

logging.basicConfig(
    filename='stock_price.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p'
)
logging.getLogger('').addHandler(logging.StreamHandler())

QUERY_URL_FMT = "http://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes=%s"

def is_price_row(row):
    return 'class' in row.attrs

def get_ASX_stock_prices(codes):
    '''Get stock prices from ASX site (http://www.asx.com.au)'''
    page = r.get(QUERY_URL_FMT % '+'.join(codes)).content.decode()
    soup = bs4.BeautifulSoup(page, 'html.parser')
    rows = list(row for row in soup.find_all('tr') if is_price_row(row))
    return {row.find('th').text.strip(): row.find('td').text.strip() for row in rows}


def get_NZX_stock_prices(codes):
    page = r.get('https://www.nzx.com/markets/nzsx/securities')
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    prices = {}
    for security in soup.find_all('tr')[1:]:
        # TODO refactor to get specific nzx stock
        code, _, price, *_ = [aspect.text.strip('$\n') for aspect in security.find_all('td')]
        if code in codes:
            prices[code] = price
    return prices


def read_stock_codes():
    codes = {}
    with open('./stock_codes.csv', encoding='utf-8-sig') as f:
        for code in f.readlines():
            stock, market = code.strip().split('.')
            codes.setdefault(market, []).append(stock)
    return codes


def main(argv):
    if len(argv) < 2:
        path = './fmt_stock_prices.csv'
    else:
        path = argv[1]

    # Get stock codes
    logging.info("Reading stock codes")
    try:
        all_codes = read_stock_codes()
    except:
        logging.error("Failed to read stock prices: The file 'stock_codes.csv' is missing or malformed")
        exit()
    asx_codes = all_codes.setdefault('AX', [])
    nzx_codes = all_codes.setdefault('NZ', [])
    logging.info("Successfully read stock codes")

    # Get stock prices
    logging.info("Getting NZX stock prices")
    try:
        NZX_prices = get_NZX_stock_prices(nzx_codes)
    except:
        logging.error("Failed to retrieve NZX stock prices")
    logging.info("Successfully got NZX stock prices")

    logging.info("Getting ASX stock prices")
    try:
        ASX_prices = get_ASX_stock_prices(asx_codes)
    except:
        logging.error("Failed to retrieve ASX stock prices")
    logging.info("Successfully got ASX stock prices")

    all_prices = dict(NZX_prices, **ASX_prices)

    # Write to file for first time
    if not os.path.isfile(path):
        logging.info("Stock prices file not found: Creating new one at %s" % os.path.abspath(path))
        with open(path, 'w', newline='') as f:
            csvwriter = csv.writer(f)
            codes = sorted(all_prices.keys())
            codes_market = []
            for code in codes:
                if code in asx_codes:
                    codes_market.append('ASX')
                else:
                    codes_market.append('NZX')
            csvwriter.writerow(['Stock Exchange', *codes_market])

            # Write codes
            csvwriter.writerow(['Date / Code', *codes])

    # Add new values
    # TODO Try refactor with numpy
    logging.info("Adding current stock prices")
    with open(path, 'a', newline='') as f:
        # Write date + price
        # TODO Check if today's prices are already saved
        csvwriter = csv.writer(f)
        today_date = format(datetime.now(), '%m/%d/%Y')
        prices = [price for code, price in sorted(all_prices.items())]
        csvwriter.writerow([today_date, *prices])
        logging.info("Written")
    logging.info("Complete")


if __name__ == "__main__":
    main(sys.argv)
