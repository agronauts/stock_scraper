#!/usr/bin/python3
import bs4
import requests
import csv
import logging
import sys

from datetime import date, datetime

#logging.basicConfig(filename='stock_price.log', level=logging.DEBUG)
logging.StreamHandler(sys.stdout).setLevel(logging.DEBUG)

with open('/home/patrick/Python/stock_scraper/scraper_app/nzx_stock_prices.csv', 'a') as f:
    csvwriter = csv.writer(f)
    date = format(datetime.now(), '%Y-%m-%d %H:%M:%S')
    page = requests.get('https://www.nzx.com/markets/nzsx/securities')
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    for security in soup.find_all('tr')[1:]:
        code, _, price, *_ = [aspect.text.strip('$\n') for aspect in security.find_all('td')]
        csvwriter.writerow([date, code, price])
