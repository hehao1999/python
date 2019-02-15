from requests import Request

from wechat.settings import TIMEOUT


class WechatRequest(Request):
    """
    :param callback: 回调函数
    :param need_proxy: 是否需要代理
    :param fail_time: 失败次数
    :param timeout: 超时时间
    """
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=TIMEOUT):
        Request.__init__(self, method, url, headers)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.timeout = timeout