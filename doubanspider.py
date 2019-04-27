import requests
import urllib
from bs4 import BeautifulSoup

def get_page():
    pass

def parse_data():
    pass

def save_data():
    pass

def main(page_tag_lists):
    lists_data = []
    page_num = 0
    for book_tag in page_tag_lists:
        while(1):
            url = 'http://www.douban.com/tag' + urllib.quote(book_tag)+'/book?start='+str(page_num*15)
            html = get_page(url)
            list_data = parse_data(html)
            lists_data.append(list_data)