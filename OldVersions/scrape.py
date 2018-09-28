import urllib
from bs4 import BeautifulSoup
import requests
import re

from collections import namedtuple

BASE_URL = "https://www.amazon.com/s/field-keywords=%s"
DEFAULT_SEARCH = "9780316040341"

Product = namedtuple('Product', ['link', 'title'])

TEST_ITEMS = [
    Product("https://www.google.com", "Title Example A"),
    Product("https://www.google.com", "Title Example B"),
    Product("https://www.google.com", "Title Example C"),
    Product("https://www.google.com", "Title Example D")
]

class ScrapeAmazon:
    # def getPage(url):
    #     r = requests.get(url)
    #     soup = BeautifulSoup(r.text, 'html.parser')
    #     return soup

    # def getPageLinks(soup):
    #     items = soup.find_all('a', attrs={'class': 'a-text-normal', 'href': re.compile(".*amazon.*")})
    #     links = list(set([item['href'] for item in items if item.has_attr('href')]))
    #     return links

    # def scrapePage(url):
    #     soup = ScrapeAmazon.getPage(url)
    #     links = ScrapeAmazon.getPageLinks(soup)
    #     return links

    # def searchPageLinks(param):
    #     url = BASE_URL % param
    #     return ScrapeAmazon.scrapePage(url)

    def getItems(param):
        url = BASE_URL % param
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('a', attrs={'class': 'a-text-normal', 'href': re.compile(".*amazon.*")})
        print("NUM SCRAPED = ", len(items))
        items_list = []
        for item in items:
            if item.has_attr('href'):
                prod = Product(item['href'],item['href'])
                items_list.append(prod)
        return items_list
