'''Get stock prices from ASX site (http://www.asx.com.au)'''

QUERY_URL_FMT = "http://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes=%s"


import bs4
import requests as r

def is_price_row(row):
    return 'class' in row.attrs

def get_stock_prices(codes):
    page = r.get(QUERY_URL_FMT % '+'.join(codes)).content.decode()
    soup = bs4.BeautifulSoup(page, 'html.parser')
    rows = list(row for row in soup.find_all('tr') if is_price_row(row))
    return {row.find('th').text.strip(): row.find('td').text.strip() for row in rows}


codes = ['BEN', 'MCY', 'ACX', 'WHC']
print(get_stock_prices(codes))