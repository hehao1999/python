from pickle import dumps, loads
from redis import StrictRedis

from wechat.wechatrequest import WechatRequest
from wechat.settings import *


class RequestQueue():
    def __init__(self):
        """
        初始化RedisDB
        """
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)

    def add(self, request):
        """
        队列末添加序列化的Request
        :param request: 请求对象
        :return:
        """
        if isinstance(request, WechatRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))  # rpush在列表末尾添加值
        return False

    def pop(self):
        """
        取出下一个Request并反序列化
        :return:
        """
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))  # lpop返回并删除键名为name的列表的首元素
        else:
            return False

    def empty(self):
        """
        :return: 列表是否为空
        """
        return self.db.llen(REDIS_KEY) == 0
