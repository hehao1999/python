"""爬取西刺https代理ip"""
import requests
import random

from bs4 import BeautifulSoup

with open('ip_pool.txt', 'r') as f:  # ip池
    ip_table = eval(f.read())
print(ip_table)


def ip_pool(ip_table):
    url = 'https://www.xicidaili.com/wn/{0}'
    ip_list = []
    for i in range(1, 52):
        r1 = requests.get(
            url=url.format(i),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Fire'
            },
            proxies={'https': 'https://115.151.5.168:9999'},  # eval(random.choice(ip_table))
            timeout=10
        )
        s1 = BeautifulSoup(r1.text, 'html.parser')
        ip_table = s1.find('table', id='ip_list').find_all('tr')[1:]
        for ip in ip_table:
            ip_port = ip.find_all('td')[1:3]
            ip = ip_port[0].text
            port = ip_port[1].text
            result = "{'https':'https://%s:%s'}" % (ip, port)
            ip_list.append(result)
    return ip_list


with open('ip_pool.txt', 'w', encoding='utf-8') as f:
    f.write(str(list(ip_pool(ip_table))))
