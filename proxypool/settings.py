"""
    配置文件
"""
# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = ''

REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 10000

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 20

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API配置，进入http://API_HIST:API_PORT/random即可获取一个合格的随机代理
API_HOST = '127.0.3.1'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 100