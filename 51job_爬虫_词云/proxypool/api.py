"""
    接口模块，非远程服务器无法使用
"""
from flask import Flask, g
from proxypool.proxydb import RedisClient

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
        return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    # 返回随机代理
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    # 返回代理池总量
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()
