import urllib
from bs4 import BeautifulSoup
import requests
import re
from user_agent import generate_user_agent
from collections import namedtuple, deque
from multiprocessing import Queue

from PyQt5.QtCore import QThread
import PyQt5.QtCore as qtc

Product = namedtuple('Product', ['link', 'title'])

BASE_URL = "https://www.amazon.com/s/field-keywords=%s"

headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}

def getItemLinks(param):
        url = BASE_URL % param
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all(
            'a', attrs={'class': 'a-text-normal', 'href': re.compile(".*amazon.*")})
        
        print("ITEMS == ", len(items))

        items_list = []
        for item in items:
            if item.has_attr('href') and item.has_attr('title'):
                link = item['href']
                title = item['title']
                if link[0] is '/':
                    link = 'https://www.amazon.com' + link
                prod = Product(link, title)
                items_list.append(prod)
        return items_list


class ScrapeThread(QThread):
    dataSig = qtc.pyqtSignal(list)
    def __init__(self):
        self.queue = deque()
        super().__init__()

    def __del__(self):
        self.wait()

    def pushTask(self, param):
        self.queue.append(param)

    def run(self):
        while True:
            try:
                param = self.queue.popleft()
                items = getItemLinks(param)
                self.dataSig.emit(items)
            except IndexError:
                pass


if __name__ == '__main__':
    items = getItemLinks('tv')
    for item in items:
        print (item.title)
