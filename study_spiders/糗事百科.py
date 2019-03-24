import requests
from bs4 import BeautifulSoup
import re
import os


def validateTitle(title):
    """去除文件名中不能做标题的符号"""
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


url = 'https://www.qiushibaike.com/text/'  # 糗事百科链接
r1 = requests.get(url)
s1 = BeautifulSoup(r1.text, 'html.parser')
content = s1.find(name='div', attrs={'class': 'col1', 'id': 'content-left'})
content_list = content.find_all(name='div', attrs={'class': re.compile('article block untagged mb15 typs_.+')})  # 糗事列表
for i in content_list:
    user = i.find('img').get('alt')
    head_img = 'https:' + i.find('img').get('src')
    funny = i.find(name='span', attrs={'class': 'stats-vote'}).find(name='i', attrs={'class': 'number'}).text
    comment = i.find(name='span', attrs={'class': 'stats-comments'}).find(name='i', attrs={'class': 'number'}).text
    link = 'https://www.qiushibaike.com' + i.find(name='a', attrs={'class': 'contentHerf'}).get('href')
    summary = i.find('div', class_='content').find(name='span', class_='').text
    print(user, head_img, funny, comment, link)
    print(summary)

    file_name0 = os.getcwd() + '\糗事百科\\' + validateTitle(user) + '.txt'
    with open(file_name0, 'w', encoding='utf-8') as f:
        f.write('用户：' + user + '\n')
        f.writelines('头像链接：' + head_img + '\n')
        f.writelines('好笑数：' + funny + '\n')
        f.writelines('评论数：' + comment + '\n')
        f.writelines('链接：' + link + '\n')
        f.write(summary + '\n')

    pic_response = requests.get(head_img)
    file_name = os.getcwd() + '\糗事百科\\' + validateTitle(user) + '.jpg'
    print(file_name)
    with open(file_name, 'wb') as f:
        f.write(pic_response.content)
