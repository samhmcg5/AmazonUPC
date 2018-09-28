import urllib
from bs4 import BeautifulSoup
import requests
import re
from scrape import ScrapeAmazon

# page = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=9780316040341'
# page = 'https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Dstripbooks&field-keywords=outliers'
# page = 'https://www.amazon.com/s/field-keywords=9780316040341'
page = 'https://www.amazon.com/s/field-keywords=vacuum'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

# r = requests.get(page)
# soup = BeautifulSoup(r.text, 'html.parser')
# print(soup)
# # items = soup.find_all('a', attrs={'class':'a-text-normal', 'href':re.compile(".*amazon.*")})
# items = soup.find_all('a', attrs={'class':'a-text-normal'})
# print(items)
# links = list(set([item['href'] for item in items if item.has_attr('href')]))


links = ScrapeAmazon.getItems('vacuum')

for link in links:
    print(link.title)
