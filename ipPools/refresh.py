import pymysql
import requests
import os
from requests.adapters import HTTPAdapter


class RefreshProxy(object):
	'''刷新数据库中的代理'''
    def __init__(self, header):
        self.header = header

    def check(self, single_proxy):
        '''检测代理是否可用'''
        print("run child %s" % (os.getpid()))
        db = pymysql.connect(host="localhost", user="root", password="123456", db="proxy", charset="utf8")
        cur = db.cursor()
        session = requests.Session()
        '''设置最大试链接次数'''
        adapter = requests.adapters.HTTPAdapter(max_retries=2)
        session.mount("http", adapter)
        session.mount("https", adapter)
        proxyToCheck = {
            'http': 'http://' + single_proxy[0],
            'https': 'https://' + single_proxy[0]
        }
        try:
            '''对目标网站进行链接测试，可用的代理存入数据库'''
            session.get(url='http://www.23us.so/files/article/html/13/13196/5345972.html', headers=self.header,
                        proxies=proxyToCheck, timeout=2)
            sql = "insert into proxy(proxy)values(%s);"
            cur.execute(sql, single_proxy)
            db.commit()
            print("验证成功")
        except Exception as e:
            print(e)
        db.close()

