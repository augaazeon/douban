import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import random
import time
import pymongo
client = pymongo.MongoClient(host='127.0.0.1',port=27017)
db = client['douban']
collection = db['book']
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'
]
headers = {
    'User-Agent': random.choice(user_agents)
}

def get_items_page(keyword,page_num):
    base_url = 'https://book.douban.com/tag/'
    url = base_url + quote(keyword) + '/?start=' + str(page_num*20)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200 :
            print(response.status_code,response.url)
            return response.text
    except requests.ConnectionError:
        print('请求失败')

def parse_page(html):
    soup = BeautifulSoup(html,'lxml')
    for info in soup.select('.info'):
        book_name = info.select('h2 a')[0]['title']
        book_pub = info.select('.pub')[0].get_text().strip().replace(' ', '')
        rating_people = info.select('.star .pl')[0].get_text().strip()
        book_info = {
            'book_name':book_name,
            'book_pub':book_pub,
            'rating_people':rating_people
        }
        yield book_info

def save_data(book_info):
    collection.insert(book_info)


def main(keyword_list):
    for keyword in keyword_list:
        for page_num in range(0,50):
            html = get_items_page(keyword,page_num)
            time.sleep(2)
            book_infos = parse_page(html)
            for book_info in book_infos:
                save_data(book_info)
                print(book_info)

from multiprocessing.pool import Pool

groups = (['心理', '判断与决策', '算法', '数据结构', '经济', '历史'])
if __name__ == '__main__':
    keyword_list = ['心理', '判断与决策', '算法', '数据结构', '经济', '历史']
    # main(keyword_list)
    pool = Pool()
    # groups = (keyword_list)
    pool.map(main,keyword_list)
    pool.close()
    pool.join()


