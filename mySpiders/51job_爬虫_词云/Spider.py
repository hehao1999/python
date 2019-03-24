"""
    爬虫
"""
import requests
import pymongo
from pyquery import PyQuery as pq

import proxy
from config import *

# 初始化
base_url = "http://search.51job.com/list/000000,000000,0000,00,{time},{salar},{keywords},2,{page}.html?lang=c&stype=1" \
           "&postchannel=0000&workyear={workyear}&cotype={cotype}&degreefrom={degreefrom}&jobterm={jobterm}&companysiz" \
           "e={companysize}&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=7&dibiaoid=0&address=&line=&spec" \
           "ialarea=00&from=&welfare={welfare}".format(time=TIME, salar=SALAR, keywords=KEYWORDS, workyear=WORKYEAR,
                                                       cotype=COTYPE, degreefrom=DEGREEFROM, jobterm=JOBTERM,
                                                       companysize=COMPANSIZE, welfare=WELFARE, page='{page}')

headers = {
    'Host': 'search.51job.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}


def get_proxy():
    """
    获取随机代理
    :return:
    """
    try:
        r = requests.get(proxy.PROXY_URL)
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
    获取总页数
    :return: page
    """
    try:
        url = base_url.format(page=1)
        response = requests.get(url=url, headers=headers, proxies=proxy.proxies, timeout=8)
        print(url, response.status_code)
        response.encoding = 'gbk'
        page = int(pq(response.text).find('span.td:nth-child(2)').text()[1:-4])
        print('共{0}页'.format(page))
        return page
    except Exception as e:
        print('get_page error', 'try again')
        proxy.proxies = get_proxy()
        return get_page()


def parse_list(url, try_num):
    """
    解析工作表
    :param url: url
    :return: parse_url(url), save_to_mongodb(data)
    """
    try:
        response = requests.get(url=url, headers=headers, proxies=proxy.proxies, timeout=8)
        print(url, response.status_code)
        response.encoding = 'gbk'
        doc = pq(response.text)
        items = doc('#resultList .el').items()
        for item in items:
            if item.find('.title'):
                continue
            if item.attr('class_') == 'el':
                data = {
                    'title': item.find('span:nth-child(3) > a:nth-child(1)').text(),
                    'url': item.find('span:nth-child(3) > a:nth-child(1)').attr('href'),
                    'company': item.find('span:nth-child(2) > a:nth-child(1)').text(),
                    'company_url': item.find('span:nth-child(2) > a:nth-child(1)').attr('href'),
                    'location': item.find('span.t3').text(),
                    'salar': item.find('span.t4').text(),
                    'time': item.find('span.t5').text(),
                }
                parse_url(data['url'], 1)
                save_to_mongodb(data)
    except Exception as e:
        print('parse_list error', '\ntry again')
        proxy.proxies = get_proxy()
        if try_num <= 10:
            parse_list(url, try_num + 1)


def parse_url(url, try_num):
    """
    获取具体工作信息
    :param url:
    :return: save_to_txt(data)
    """
    try:
        response = requests.get(url=url, headers=headers, proxies=proxy.proxies, timeout=8)
        print(url, response.status_code)
        response.encoding = 'gbk'
        doc = pq(response.text)
        data = doc('.job_msg').text().replace('岗位职责：', '').replace('任职要求：', '').replace('微信分享', '').strip()
        return save_to_txt(data, 1)
    except Exception as e:
        print("parse_url error", '\ntry again')
        proxy.proxies = get_proxy()
        if try_num <= 10:
            parse_url(url, try_num + 1)


def save_to_txt(data, try_num):
    """
    详细信息写入txt文本
    :param data:
    :param try_num:
    :return:
    """
    try:
        with open(TXT, 'a+', encoding='gbk', errors='ignore') as f:
            f.write(data)
    except Exception as e:
        print("save_to_txt error", e.args, '\ntry again')
        if try_num <= 10:
            save_to_txt(data, try_num + 1)


def save_to_mongodb(data):
    """
    存储到数据库
    :param data:
    :return:
    """
    try:
        if data:
            client = pymongo.MongoClient(host='localhost', port=27017)
            db = client[CLIENT]
            collection = db[COLLECTION]
            collection.insert_one(data)
    except Exception as e:
        print('save_to_mongodb error', e.args)


def run():
    """
    单线程运行
    :return:
    """
    proxy.proxies = get_proxy()
    page = get_page()
    for i in range(page):
        print("爬取第{}页".format(i + 1))
        url = base_url.format(page=i + 1)
        parse_list(url, 1)


"""
    多线程模式
"""
import threading


def div_page(page):
    """
    分配页数
    :param page:
    :return:
    """
    return int(page / 2)


def run2(page1, page2):
    """
    爬取方式2
    :param page1:
    :param page2:
    :return:
    """
    for i in range(page1, page2):
        print("爬取第{}页".format(i + 1))
        url = base_url.format(page=i + 1)
        parse_list(url, 1)


def run_fast():
    """
    开启多线程
    :return:
    """
    proxy.proxies = get_proxy()
    page = get_page()
    page2 = div_page(page)
    t1 = threading.Thread(target=run2, args=(0, page2), name='Thread1')
    t2 = threading.Thread(target=run2, args=(page2 + 2, page + 1), name='Thread2')
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    """
    tip: 如需使用代理请先运行代理池并确保代理池中有合法代理
    """
    if MUL_THREAD == False:
        run()
    else:
        run_fast()
