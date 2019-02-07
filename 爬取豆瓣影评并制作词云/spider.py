import requests
from bs4 import BeautifulSoup


def check(url, ip):
    try:
        requests.get(url, proxies=eval(ip), timeout=3)
        print("代理:选择完毕")
        return True
    except Exception:
        return False


with open('ip_pool.txt', 'r') as f:  # ip池
    ip_list = eval(f.read())

for i in ip_list:
    if check('https://www.douban.com/', i):
        proxies = i
        print('使用代理：', proxies)
        break
    continue

url = 'https://movie.douban.com/subject/30155194/comments?start={0}&limit=20&sort=new_score&status=P'
url_list = [url.format(i * 10) for i in range(0, 101, 2)]
txt = []

session = requests.session()
for i, u in enumerate(url_list):
    r1 = session.get(
        url=u,
        proxies=eval(proxies),
    )
    soup = BeautifulSoup(r1.text, 'html.parser')
    comment = soup.find('div', id='comments', class_='mod-bd')
    if comment:
        comments = comment.find_all('span',class_='short')
        for span in comments:
            txt.append(span.text)
            print(span.text)
    else:

        break
print(txt)
with open('蔡娘娘不欺负女孩子短评.txt', 'w', encoding='utf-8') as f:
    for i in txt:
        f.write(i+'\n')
    print('over')
