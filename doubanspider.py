import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import random
import time
import pymongo
from multiprocessing.pool import Pool

client = pymongo.MongoClient(host='120.17.34.25',port=27017)
db = client['douban']
collection = db['book5']
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'
]
headers = {
    'User-Agent': random.choice(user_agents),
    #'Cookie':'bid=7Of0zrNMdO0; douban-fav-remind=1; gr_user_id=fa4c2374-7733-405f-a7eb-9d0bd0604ac1; _vwo_uuid_v2=D540F0DAFDD89EDC17D9F171F6E94A0DB|7a29a18f06b78043c03e5dc37eb5af4e; __yadk_uid=DWCrq7cXAORSg5h6PsJKQCV8nrVtgQl5; ct=y; ll="118296"; ap_v=0,6.0; __gads=ID=c01194ed390ccdfc:T=1557806840:S=ALNI_MYjafegWIT372pmkKTolclKVgdLww; viewed="3259440"; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=78b3570b-4737-4a22-8f91-43e519b9cc27; gr_cs1_78b3570b-4737-4a22-8f91-43e519b9cc27=user_id%3A0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_78b3570b-4737-4a22-8f91-43e519b9cc27=true; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1557811797%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; dbcl2="153572358:vYSCBc2W+/E"; ck=zdX6; _pk_id.100001.3ac3=ef907b26f27f1ba4.1557806841.2.1557812855.1557806906.; push_noty_num=0; push_doumail_num=0'

}


def get_items_page(url):

        try:
            response = requests.get(url,headers=headers)
            if response.status_code == 200 :
                print(response.status_code,response.url)
                return response.text
        except requests.ConnectionError:
            print('请求失败')

def parse_page(html):
    soup = BeautifulSoup(html,'lxml')
    tag = soup.select('#content h1')[0].get_text()
    for info in soup.select('.info'):
        book_name = info.select('h2 a')[0]['title']
        book_pub = info.select('.pub')[0].get_text().strip().replace(' ', '')
        rating_people = info.select('.star .pl')[0].get_text().strip()
        book_info = {
            'tag':tag,
            'book_name':book_name,
            'book_pub':book_pub,
            'rating_people':rating_people
        }
        yield book_info

def save_data(book_info):
    collection.insert(book_info)

def get_url(keyword_list):
    for keyword in keyword_list:
        base_url = 'https://book.douban.com/tag/' + quote(keyword)
        for page_num in range(0, 50):
            url = base_url + '/?start=' + str(page_num * 20)
            yield url

def main(url):
    for page_num in range(0, 50):
        html = get_items_page(url)
        time.sleep(2)
        book_infos = parse_page(html)
        for book_info in book_infos:
            save_data(book_info)
            print(book_info)

keyword_list = ['心理', '判断与决策', '算法', '数据结构', '经济', '历史']
if __name__ == '__main__':
    pool = Pool()
    url_list = get_url(keyword_list)
    # for url in url_list:
    #     print(url)
    pool.map(main, url_list)
    pool.close()
    pool.join()


