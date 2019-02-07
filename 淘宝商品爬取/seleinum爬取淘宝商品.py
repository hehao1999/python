import re
import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from mongo_cfg import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

url = 'https://www.taobao.com/'
goods = u'美食'
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def search(url, goods):
    try:
        browser.get(url)
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="q"]')))
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="J_TSearchForm"]/div[1]/button')))
        input.send_keys(goods)
        submit.click()

        total = WebDriverWait(browser, 300).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        return re.match('.*?(\d+).*', total.text).group(1)
    except TimeoutException:
        return search(url, goods)


def next_page(page_num):
    print('正在翻页', page_num)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/div[2]/input')))
        submit = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/div[2]/span[3]')))
        input.clear()
        input.send_keys(page_num)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), page_num))
        print('开始爬取第{}页商品'.format(page_num))
        get_goods()
    except TimeoutException:
        print('出错了')
        next_page(page_num)  # 采用递归，继续访问超时的页面


def get_goods():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        good = {
            'image': 'https:' + item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(good)
        save_to_mongo(good)


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MongoDB成功', result)
    except Exception:
        print('存储到MongoDB失败', result)


def main():
    total = int(search(url, goods))
    for i in range(1, total + 1):
        next_page(str(i))
    browser.close()


if __name__ == '__main__':
    main()
