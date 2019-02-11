"""
    存储模块，采用REDIS数据库
"""
import re
import redis
from random import choice

from proxypool.error import PoolEmptyError
from proxypool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.settings import MAX_SCORE, MIN_SCORE, INITIAL_SCORE


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db_password=REDIS_PASSWORD):
        # 连接数据库，初始化
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWORD,
                                    decode_responses=True)  # decode_responses=True,写入的键值对中的value为str类型，不加这个参数写入的则为字节类型

    def add(self, proxy, score=INITIAL_SCORE):
        # 添加代理
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)  # p277 如果数据库中不存在proxy，则向REDIS_KEY中添加（score,proxy）

    def random(self):
        # 随机选取最高分数的代理，若不存在则按照排名选取
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)  # 返回REDIS_KEY中位于0~100的所有元素的从大到小排列的列表
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        # 对未通过测试的代理进行减分和删除处理
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, 'score-1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, 'remove')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        # 判断代理是否已经存在
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        # 将代理设置为最高分
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)  # 如果proxy存在就会更新

    def count(self):
        # 返回代理池中代理数目
        return self.db.zcard(REDIS_KEY)

    def all(self):
        # 返回库中全部代理列表
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        # 批量获取，返回代理列表，参数有开始结束所索引
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)