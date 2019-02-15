from requests import Session
from urllib.parse import urlencode
import requests
import time

from wechat.mysql import MySQL
from pyquery import PyQuery as pq
from requests import ReadTimeout, ConnectionError

from wechat.settings import *
from wechat.requestqueue import RequestQueue
from wechat.wechatrequest import WechatRequest


class Spider():
    base_url = 'http://weixin.sogou.com/weixin'
    keyword = '软件工程'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'SUV=00925557718609255ADAEA2A76556959; CXID=169F175714C5047FC1C1EE408C807F9E; SUID=250986714C238B0A5ADAF598000ADCD8; ssuid=3311322898; sw_uuid=4104253341; sg_uuid=7321830132; ABTEST=0|1548162898|v1; IPLOC=CN4305; weixinIndexVisited=1; LSTMV=569%2C28; LCLKINT=4917; ld=rkllllllll2tSeWWlllllVe4VicllllltNZTflllll9lllllVklll5@@@@@@@@@@; ad=Zlllllllll2tqOt8lllllVeQq8GllllltNZCeZllll9llllllZlll5@@@@@@@@@@; ppinf=5|1550048619|1551258219|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTMlODAlODIlRTMlODAlODIlRTMlODAlODJ8Y3J0OjEwOjE1NTAwNDg2MTl8cmVmbmljazoyNzolRTMlODAlODIlRTMlODAlODIlRTMlODAlODJ8dXNlcmlkOjQ0Om85dDJsdU9zVlJqdVZBVHlScFRDWGs5WkxzTVFAd2VpeGluLnNvaHUuY29tfA; pprdig=aGkoylJ6avTniGHzFE8avM4eSP8bwqZyAxiFmu_8kumqTT_2y2BtQ9e5OTw0jnoaMXe4TKO1c2RLu6ItpJa1OijauTJSzL_-WwtRMMe4dURiBxCEctCaGR3S8CAt4DcTHjajwJRimfEryxiTeCvR1BK1gcasRj_-U1aCT9JqHwE; sgid=24-39260611-AVxj3WsnwPQs0icWjpVhU3r8; SNUID=950FE9473530B7E39D1E32853668535E; sct=12; JSESSIONID=aaaliCbDBYcuoffL1U7Hw; ppmdig=15501472440000004c2ee668a1d884094cc2abc098cabf57',
        'Host': 'weixin.sogou.com',
        'Referer': 'https: // weixin.sogou.com /',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    session = Session()
    queue = RequestQueue()
    mysql = MySQL()

    def get_proxy(self):
        """
        获取随机代理
        :return:
        """
        try:
            r = requests.get(PROXY_URL)
            if r.status_code == 200:
                print("get proxy successfully:", r.text)
                return r.text
            print("get proxy:None")
            return None
        except requests.ConnectionError:
            print("get proxy:None")
            return None

    def parse_index(self, response):
        """
        解析索引页(文章表)
        :param response: 响应
        :return: 新的响应
        """
        doc = pq(response.text)
        items = doc('.news-box .news-list li .txt-box h3 a').items()  # 生成链接的生成器
        for item in items:
            url = item.attr('href')
            weixin_request = WechatRequest(url=url, callback=self.parse_detail)  # 遍历解析每一篇文章
            yield weixin_request
        # 下一页
        next_page = doc('#sogou_next').attr('href')
        if next_page:
            url = self.base_url + str(next_page)
            weixin_request = WechatRequest(url=url, callback=self.parse_index, need_proxy=True)  # 解析索引页（文章表）
            time.sleep(2)
            yield weixin_request

    def parse_detail(self, response):
        """
        解析详情页
        :param response: 响应
        :return: 微信公众号文章
        """
        doc = pq(response.text)
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#post-date').text(),
            'nickname': doc('#js_profile_qrcode > div > strong').text(),
            'wechat': doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        }
        print(data)
        yield data

    def request(self, wechat_request):
        """
        执行请求,将PreparedRequest对象执行为请求
        :param weixin_request: 请求
        :return: 响应
        """
        try:
            if wechat_request.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    proxies = {
                        'http': 'http://' + proxy,
                        'https': 'https://' + proxy
                    }
                    # 返回一个PreparedRequest对象（这样就可以把请求当作独立的对象看待，而不是立即执行，进行队列调用时非常方便），还可以进行处理
                    # 要获取一个带有状态的 PreparedRequest，用 Session.prepare_request() 取代 Request.prepare() 的调用，然后使用send发送请求
                    # 在这里就相当于get
                    return self.session.send(wechat_request.prepare(),
                                             timeout=wechat_request.timeout, proxies=proxies)
            return self.session.send(wechat_request.prepare(), timeout=wechat_request.timeout)
        except (ConnectionError, ReadTimeout) as e:
            print('Error:', e.args)
            return False

    def schedule(self):
        """
        请求调度
        :return:
        """
        while not self.queue.empty():
            wechat_request = self.queue.pop()
            callback = wechat_request.callback
            print('Schedule:', wechat_request.url)
            response = self.request(wechat_request)
            if response and response.status_code in VALID_STATUES:
                results = list(callback(response))
                if results:
                    for result in results:
                        print('New Result', type(result))
                        if isinstance(result, WechatRequest):
                            self.queue.add(result)
                            print("add成功")
                        if isinstance(result, dict):
                            self.mysql.insert('spiders', result)
                            print("insert成功")
                else:
                    self.error(wechat_request)
            else:
                self.error(wechat_request)

    def error(self, wechat_request):
        """
        错误处理
        :param weixin_request: 请求
        :return:
        """
        wechat_request.fail_time = wechat_request.fail_time + 1
        print('Request Failed', wechat_request.fail_time, 'Times', wechat_request.url)
        if wechat_request.fail_time < MAX_FAILED_TIME:
            self.queue.add(wechat_request)

    def start(self):
        """
        初始化
        """
        self.session.headers.update(self.headers)
        start_url = self.base_url + '?' + urlencode({'query': self.keyword, 'type': 2})
        print('start_url:', start_url)
        wechat_request = WechatRequest(url=start_url, callback=self.parse_index, need_proxy=True)
        self.queue.add(wechat_request)

    def run(self):
        """
        入口
        :return:
        """
        self.start()
        self.schedule()

if __name__ == '__main__':
    spider = Spider()
    spider.run()
