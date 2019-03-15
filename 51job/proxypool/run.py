"""
    使用方法，运行程序，进入http://API_HIST:API_PORT/random即可获取一个合格的随机代理
"""

from proxypool.scheduler import Scheduler
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')   #改变标准输出的默认编码为utf-8


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()
