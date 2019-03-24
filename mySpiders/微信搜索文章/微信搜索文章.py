import re
import requests
import os
import random
from bs4 import BeautifulSoup


def validateTitle(title):
    """去除文件名中不能做标题的符号"""
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def check(ip, url):
    """检查ip是否可用"""
    try:
        requests.get(url, proxies=eval(ip), timeout=5)
        return True
    except Exception:
        return False


def get_proxies(ip_list, url0):
    """取得可用"""
    while True:
        ip_ = random.choice(ip_list)
        if check(ip_, url0.format(1)):
            return ip_


headers = {  # 请求头
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'SUV=00925557718609255ADAEA2A76556959; CXID=169F175714C5047FC1C1EE408C807F9E; SUID=250986714C238B0A5ADAF5'
              '98000ADCD8; ssuid=3311322898; sw_uuid=4104253341; sg_uuid=7321830132; ABTEST=0|1548162898|v1; IPLOC=CN43'
              '05; weixinIndexVisited=1; SNUID=429D75DBA9AF29A26F1455CBAAE3D4C7; LSTMV=569%2C28; LCLKINT=4917; ld=rklll'
              'lllll2tSeWWlllllVe4VicllllltNZTflllll9lllllVklll5@@@@@@@@@@; sct=4; JSESSIONID=aaakaa3U23DcZedZgU8Cw',
    'Host': 'weixin.sogou.com',
    'Referer': 'https://weixin.sogou.com/weixin?oq=&query=%E7%89%A9%E8%81%94%E7%BD%91&_sug_type_=1&sut=0&lkt=0%2C0%2C0&'
               's_from=input&ri=1&_sug_=n&type=2&sst0=1548163203328&page=2&ie=utf8&p=40040108&dp=1&w=01015002&dr=1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safa'
                  'ri/537.36'
}  # 请求头
url0 = 'https://weixin.sogou.com/weixin?oq=&query=%E7%89%A9%E8%81%94%E7%BD%91&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from' \
       '=input&ri=1&_sug_=n&type=2&sst0=1548163203328&page={0}&ie=utf8&p=40040108&dp=1&w=01015002&dr=1'  # 初始url，包含链接
url0_list = []  # 文章页列表
url_list = []  # 存储每个文章页的微信文章链接
title_list = []  # 存储微信文章标题

with open('ip_pool.txt', 'r') as f:  # ip池
    ip_list = eval(f.read())

for i in range(1, 12):  # 微信文章合集页
    url0_list.append(url0.format(str(i)))

"""获取微信文章链接，标题"""
proxies = get_proxies(ip_list, url0)
print('proxies:OK')
for url0 in url0_list:
    try:
        r1 = requests.get(url=url0, proxies=eval(proxies), headers=headers)
        s1 = BeautifulSoup(r1.text, 'html.parser')
        ul = s1.find(name='ul', class_='news-list').find_all(name='li', id=re.compile('sogou_vr_11002601_box_\d+'))
        for i in ul:
            link = i.find(name='a', attrs={'data-z': 'art'}).get('href')
            title = i.find(name='h3').find('a').text
            title_list.append(validateTitle(title))
            url_list.append(link)
        print('url0_list:OK')
    except Exception as e:
        proxies = get_proxies(ip_list, url0)
        print('遇到错误+1', e)
        continue

for (i, j) in list(zip(url_list, title_list)):
    """爬取具体文章信息"""
    try:
        with open(os.getcwd() + '\\微信搜索文章\\' + j + '.html', 'w', encoding='utf-8') as f:
            f.write(requests.get(url=i, proxies=eval(proxies)).text)
            print('write:ok+1')
    except Exception:
        proxies = get_proxies(ip_list, i)
        print('遇到错误+1', e)
        continue

print('over')
