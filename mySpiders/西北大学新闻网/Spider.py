import requests
from pyquery import PyQuery as pq

"""
    初始化
"""
BASE_URL = 'http://news.nwu.edu.cn/home/index/articles/mid/565{}.html?page={}'
PAGES = [1, 2, 3, 5, 6]
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'news.nwu.edu.cn',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
PROXY_URL = 'http://localhost:5555/random'
PROXIES = dict()
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

def get_page():
    """
    获取每个需要爬取的网页内最大页码数列表
    :return: 页码page
    """
    try:
        for i in PAGES:
            url = BASE_URL.format(i, 1)

            response = requests.get(url, headers=HEADERS, proxies=PROXIES,timeout=10)
            print(url, response.status_code)
            if response.status_code != 200:
                PROXIES.clear()
                PROXIES.update(get_proxy())
                get_page()
            page = int(pq(response.text).find('#main > div > div > div.erji-content.fl > div.yema > div > ul > li:nth-child(12) > a').text())
            yield page
    except:
        PROXIES.clear()
        PROXIES.update(get_proxy())
        get_page()


def parse_detail(url):
    """
    获取具体文章内容
    :param url: url
    :return: 具体文章内容
    """
    try:
        response = requests.get(url, headers=HEADERS, proxies=PROXIES,timeout=10)
        print(url, response.status_code)
        if response.status_code != 200:
            PROXIES.clear()
            PROXIES.update(get_proxy())
            parse_detail(url)
        doc = pq(response.text)
        title = doc.find('.danpian-h1').text()
        info = doc.find('.danpian-h2').text()
        article = doc.find('.danpian-con').text()
        data = {
            'title': title,
            'info': info,
            'article': article
        }
        print(data)
        return data
    except:
        PROXIES.clear()
        PROXIES.update(get_proxy())
        parse_detail(url)


def get_title(page, page_count):
    """
    获取每篇文章的标题和链接
    :param page: 导航栏序号
    :param page_count: 导航栏新闻页数
    :return: None
    """
    try:
        for i in range(1, page_count + 1):
            url = BASE_URL.format(page, page_count)
            response = requests.get(url, headers=HEADERS, proxies=PROXIES,timeout=10)
            print(url, response.status_code)
            if response.status_code != 200:
                PROXIES.clear()
                PROXIES.update(get_proxy())
                get_title(page, page_count)
            doc = pq(response.text)
            items = doc('#main > div > div > div.erji-content.fl > div.erji-content-list > div > ul').find('li').items()
            for i in items:
                title = i.find('a').text()
                link = 'http://news.nwu.edu.cn' + i.find('a').attr('href')
                data = {
                    'title': title,
                    'link': link,
                }
                print(data)
                parse_detail(link)
    except:
        PROXIES.clear()
        PROXIES.update(get_proxy())
        get_title(page,page_count)


def main():
    """
    主函数，调度爬虫
    :return:
    """
    PROXIES.clear()
    PROXIES.update(get_proxy())
    pages = list(get_page())
    while not pages:
        pages = list(get_page())
    print(pages)
    for i in PAGES:
        k = 0
        for j in range(pages[k]):
            get_title(i, j)
        k+=1



if __name__ == '__main__':
    main()
