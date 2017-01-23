import bs4
import requests
import pprint
codes = ['ATM','AFC','AFT','A01C','WIN']
for code in codes:
    page = requests.get('https://www.google.com/finance?q=NZE%3A' + code)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    soup.find_all('span')
    pprint.pprint([tag.text for tag in soup.find_all('span') if 'id="ref' in str(tag) and 'l">' in str(tag)])
