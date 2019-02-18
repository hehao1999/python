import pymongo
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException as ER

"""初始化"""
# 陕西省空气质量实时发布系统
url = 'http://113.140.66.226:8024/sxAQIWeb/StationInfo.aspx?cityCode=NjEwMTAw'
# 大气污染物名称
gas_list = ['SO2', 'NO2', 'CO', 'O3', 'PM10', 'PM2_5', 'AQI']
# 地区编号
area_list = ['003A', '006A', '007A', '011A', '012A', '018A', '023A', '025A', '027A', '028A',
             '032A', '033A', '042A', '170A', '171A', '209A', '210A', '220A', '233A', '235A', '236A']
# 连接数据库
client = pymongo.MongoClient(host='localhost')
db = client.AirQuality
# 使用无头chrome浏览器打开系统，等待元素加载完成
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get(url)
wait = WebDriverWait(browser, 10)
wait.until(
    EC.visibility_of_all_elements_located(
        (By.CSS_SELECTOR, '#chartContent > div > div:nth-child(1) > svg > g:nth-child(13) > g')))


def get_detail(gas, area):
    """
    获取详细浓度信息
    :param gas:污染物Index
    :param area:地区名
    :return:None
    """
    circle_i = 0
    while circle_i < 24:
        # 此处为一个坑，不能使用webdriver的查找元素的方法，网页的自动刷新回造成错误，只能通过循环和css选择器查找
        try:
            circles = browser.find_elements_by_tag_name('circle')
            ActionChains(browser).move_to_element(circles[circle_i]).perform()
            # 此次又是一个坑，不能使用查找元素的方法判断是否移动到新的圆点，设置等待时间可以很好的避免漏选或误选
            sleep(0.5)
            time = browser.find_element_by_css_selector(
                '#chartContent > div > div:nth-child(1) > div > div > b:nth-child(1)').text
            con = browser.find_element_by_css_selector(
                '#chartContent > div > div:nth-child(1) > div > div > b:nth-child(3)').text
            data = {
                'time': time,
                gas_list[gas]: con
            }
            save_to_mongo(area, data)
            circle_i += 1
        except (TimeoutException, ER) as e:
            # 由于页面刷新引起错误时不刷新circle的Index
            print(e.args)
        except IndexError:
            #  某些时段的污染物浓度缺失
            break


def next(selector):
    """
    更换气体类型或区域
    :param selector:标签
    :return:None
    """
    try:
        tag = browser.find_element_by_css_selector(selector)
        ActionChains(browser).click(tag).perform()
        sleep(3)
    except Exception as e:
        print(e.args)
        next(selector)


def save_to_mongo(area, data):
    """
    把数据存入mongodb
    :param area: 行政区
    :param data: 获取的数据
    :return:None
    """
    try:
        collection = db[area]
        if not collection.find_one({'time': data['time']}):
            collection.insert_one(data)
            print('存储到MongoDB成功', area, data)
        else:
            collection.update_one({'time': data['time']}, {'$set': data})
            print('存储到MongoDB成功', area, data)
    except Exception as e:
        print(e.args)
        print('存储到MongoDB失败', data)


def start():
    """
    开始程序，可考虑将不同地区放在不同线程下运行提高效率
    :return: None
    """
    # 初始化污染物Index
    gas_i = 0
    # 初始化行政区Index
    area_i = 0
    while area_i < 21:
        while gas_i < 7:
            get_detail(gas_i, area_list[area_i])
            if gas_i == 6:
                break
            gas_i += 1
            next('#{0} > td:nth-child(1)'.format(gas_list[gas_i]))
        area_i += 1
        next('#\\31 {0} > td:nth-child(1)'.format(area_list[area_i]))
        gas_i = 0


if __name__ == '__main__':
    start()
    browser.close()
