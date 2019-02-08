"""爬取汽车之家新闻标题、链接、简介、图片"""
import requests
from bs4 import BeautifulSoup
import os

response = requests.get("http://www.autohome.com.cn/news/")  # 汽车之家
response.encoding = 'gbk'
soup = BeautifulSoup(response.text, "html.parser")
# print(type(soup))  # bs4.BeautifulSoup
# print(type(soup.find(id="auto-channel-lazyload-article"))) # bs4.element.Tag

lis = soup.find(id="auto-channel-lazyload-article").find_all(name='li')
for li in lis:
    if not li.find('h3'):  # if去掉空的,防止出现错误
        continue
    title = li.find('h3').text  # 标题，.text提取标签
    summary = li.find('p').text.strip('[汽车之家 行业]')  # 简介
    link = li.find('a').attrs['href'].strip(r'//')  # 链接，提取标签属性,，也可以使用.get('href')
    img = li.find('img').get('src').strip(r'//')  # 图片链接
    print(title, link, summary, img)

    pic_response = requests.get(r'https://' + img)  # 访问图片链接，注意加https://
    file_name = '{0}.jpg'.format(title)
    with open(os.getcwd() + r'\picture\\' + file_name[:3] + '.jpg', 'wb') as jpg_file:#下载图片，二进制格式，并存在当前目录的picture文件夹下，注意加了r最好还是得双写//
        jpg_file.write(pic_response.content)
