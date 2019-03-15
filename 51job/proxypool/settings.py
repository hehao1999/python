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
POOL_UPPER_THRESHOLD = 5000

# 检查周期
TESTER_CYCLE = 10
# 获取周期
GETTER_CYCLE = 10

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://search.51job.com/list/000000,000000,0000,00,9,99,GIS,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=01&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=7&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

# API配置，进入http://API_HIST:API_PORT/random即可获取一个合格的随机代理
API_HOST = 'localhost'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 200
