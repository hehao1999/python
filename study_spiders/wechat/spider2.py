import requests
import pymongo
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from requests import ReadTimeout, ConnectionError

from wechat.settings import *

base_url = 'http://weixin.sogou.com/weixin'
keyword = '软件工程'
headers = {
    'Host': 'pb.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Accept': 'image/webp,*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://weixin.sogou.com/weixin?oq=&query=%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input&ri=7&_sug_=n&type=2&sst0=1550144064585&page=2&ie=utf8&p=40040108&dp=1&w=01015002&dr=1',
    'Connection': 'keep-alive',
    'Cookie': 'SUV=00904B5671DC35C75C5405805897D937; SNUID=50C82C81F0F57024586FB693F1D943B4; IPLOC=CN4305; SUID=A039DC713320910A000000005C651995',
}
params = {
    'uigs_cl': 'first_click',
    'uigs_refer': '',
    'uigs_t': '1550145296485',
    'uigs_productid': 'vs_web',
    'terminal': 'web',
    'vstype': 'weixin',
    'pagetype': 'result',
    'channel': 'result_article',
    's_from': 'input',
    'sourceid': '',
    'type': 'weixin_search_pc',
    'uigs_cookie': 'SUID,sct',
    'uuid': '1c8646e8-dfe7-454e-ab54-92eb7741d52a',
    'query': '软件工程',
    'weixintype': '2',
    'exp_status': 'null',
    'exp_id_list': 'null',
    'wuid': '00904B5671DC35C75C5405805897D937',
    'snuid': '50C82C81F0F57024586FB693F1D943B4',
    'rn': '1',
    'login': '0',
    'uphint': '1',
    'bottomhint': '1',
    'page': '2',
    'exp_id': 'null_10-null_11-null_12-null_13-null_14-null_15-null_16-null_17-null_18-null_19',
}

start_url = 'https://weixin.sogou.com/weixin?oq=&query=%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input&ri=7&_sug_=n&type=2&sst0=1550144064585&page={0}&ie=utf8&p=40040108&dp=1&w=01015002&dr=1'
print(start_url)
session = requests.session()
queue = []


def get_proxy():
    """
    获取随机代理
    :return:
    """
    try:
        r = requests.get(PROXY_URL)
        if r.status_code == 200:
            print("get proxy successfully:", r.text)
            return {
                'http': 'http://' + r.text,
                'https': 'https://' + r.text
            }
        print("get proxy:None")
        return None
    except requests.ConnectionError:
        print("get proxy:None")
        return None


def save_to_mongo(data):
    """
    存入mongodb
    """
    if data:
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client.wechat
        collection = db.articles
        collection.insert(data)


def parse_index(url, count=1):
    """
    解析索引页(文章表)
    """
    try:
        proxies = get_proxy()
        response = session.get(url, proxies=proxies, allow_redirects=False)
        if response.status_code == 200:
            doc = pq(response.text)
            items = doc('.news-box .news-list li .txt-box h3 a').items()  # 生成链接的生成器
            for item in items:
                url = item.attr('href')
                queue.append(url)
                print("ok", url)
            # 下一页
        elif response.status_code == 301 or response.status_code == 302:
            if count == 10:
                print('try too many times:', url)
                return None
            print(count, response.status_code, url)
            return parse_index(url, count + 1)
    except Exception as e:
        print('Error:', e.args, 'try again')
        return parse_index(url, count)


def parse_detail(url, count=1):
    """
    解析详情页
    :return: 微信公众号文章
    """
    try:
        proxies = get_proxy()
        response = requests.get(url,proxies=proxies)
        if response.status_code in VALID_STATUES:
            doc = pq(response.text)
            data = {
                'title': doc('.rich_media_title').text(),
                'content': doc('.rich_media_content').text(),
                'date': doc('#post-date').text(),
                'nickname': doc('#js_profile_qrcode > div > strong').text(),
                'wechat': doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
            }
            return data
        else:
            if count == 10:
                return None
            print(count, response.status_code, url)
            return parse_detail(url, count + 1)
    except (ConnectionError, ReadTimeout) as e:
        print('Error:', e.args, 'try again')
        return parse_detail(url, count)


def start():
    for i in range(1, 2):
        parse_index(start_url.format(str(i)), 1)
    print(queue)
    while queue:
        url = queue.pop()
        detail = parse_detail(url)
        print(detail)
        save_to_mongo(detail)
    print('over')


if __name__ == '__main__':
    start()
