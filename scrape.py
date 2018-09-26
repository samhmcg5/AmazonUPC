import urllib
from bs4 import BeautifulSoup
import requests
import re

BASE_URL = "https://www.amazon.com/s/field-keywords=%s"
DEFAULT_SEARCH = "9780316040341"

class ScrapeAmazon:
    def getPage(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def getPageLinks(soup):
        items = soup.find_all('a', attrs={'class': 'a-text-normal', 'href': re.compile(".*amazon.*")})
        links = list(set([item['href'] for item in items if item.has_attr('href')]))
        return links

    def scrapePage(url):
        soup = ScrapeAmazon.getPage(url)
        links = ScrapeAmazon.getPageLinks(soup)
        return links

    def searchPageLinks(param):
        url = BASE_URL % param
        return ScrapeAmazon.scrapePage(url)


