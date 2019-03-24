"""
        爬取陕西省空气质量实时发布系统
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import os

"""爬取网页"""
url = 'http://113.140.66.226:8024/sxAQIWeb/StationInfo.aspx?cityCode=NjEwMTAw'
driver = webdriver.Chrome()



driver.get(url)
time.sleep(0.5)
page = BeautifulSoup(driver.page_source, 'lxml')


# 导入selenium中的actionchains的方法
from selenium.webdriver.common.action_chains import ActionChains
#识别需要悬停的元素

print(page)
ele = page.driver.find('g',id='balloons')
# 鼠标移到悬停元素上
ActionChains(page.driver).move_to_element(ele).perform()
time.sleep(0.5)
page2 = BeautifulSoup(driver.page_source, 'lxml')
print(page2)

driver.close()



"""网页解析"""
trs = page.find_all('tr', id=re.compile('1\d\d\dA'))
ulist = []
for tr in trs:
    ui = []
    for td in tr:
        ui.append(td.string)
    ulist.append(ui)

"""存为表格"""
f = open(os.path.abspath('.') + r'\data.csv', 'a', encoding='gbk')
test = ""
for datas in ulist:
    temp = ','.join(str(element) for element in datas)
    test += temp + '\n'
f.write(test)
f.close()
