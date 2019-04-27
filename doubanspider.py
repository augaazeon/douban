import re
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import urllib
#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]



def get_page(book_tag):
    page_num = 0
    book_lists  = []
    while(1):
        url = 'http://www.douban.com/tag/' + urllib.quote(book_tag) + 'book?start=' + str(page_num * 15)
        req = requests.get(url,headers = hds[page_num%len(hds)])
        req.encoding = 'utf-8'
        html = req.text
        book_list = parse_data(html)
        book_lists.append(book_list)
        page_num+=1
    return book_lists


def parse_data(html):
    book_list = []
    soup = BeautifulSoup(html)
    list_soup = soup.find('div',class_='mod book_list')
    for book_info in list_soup.findAll('dd'):
        title = book_info.find('a', {'class': 'title'}).string.strip()
        desc = book_info.find('div', {'class': 'desc'}).string.strip()
        desc_list = desc.split('/')
        book_url = book_info.find('a', {'class': 'title'}).get('href')

        try:
            author_info = '作者/译者： ' + '/'.join(desc_list[0:-3])
        except:
            author_info = '作者/译者： 暂无'
        try:
            pub_info = '出版信息： ' + '/'.join(desc_list[-3:])
        except:
            pub_info = '出版信息： 暂无'
        try:
            rating = book_info.find('span', {'class': 'rating_nums'}).string.strip()
        except:
            rating = '0.0'
        book_list.append([title, rating, author_info, pub_info])
    return book_list