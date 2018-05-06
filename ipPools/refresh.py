import pymysql
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

'''检测对某网站可用代理'''


class RefreshProxy(object):
    def __init__(self, header):
        self.header = header
        '''用于检测代理的目标网页'''
        self.url = 'http://www.23us.so/files/article/html/13/13196/5345972.html'

    def check(self, single_proxy):
        '''检测代理是否可用'''
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
            web_data = session.get(url=self.url, headers=self.header, proxies=proxyToCheck, timeout=2)
            web_data.encoding = "utf-8"
            if web_data.status_code == 200:
                soup = BeautifulSoup(web_data.text, "lxml")
                html_title = soup.find("title").get_text()
                '''检测是否能获得目标网站的真实内容------以顶点小说网为例子'''
                if "顶点小说网" in html_title:
                    '''将代理储存到目标网站对应表中'''
                    sql = "insert into proxy_use (proxy)values(%s);"
                    cur.execute(sql, single_proxy)
                    db.commit()
                    print("验证成功")
                else:
                    pass
            else:
                pass
        except Exception:
            pass
        finally:
            db.close()
            return
