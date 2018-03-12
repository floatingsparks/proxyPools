import pymysql
import requests
from db import main
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
}
#	更新数据库

def checkProxy(table_name, header):
    db = pymysql.connect(host='localhost', user='root', password='123456', db='ippools', charset='utf8')
    cur = db.cursor()
	# 获取最近日期
    # cur.execute('select max(time) from %s' % table_name)
    # latest_date = cur.fetchall()
    # print(latest_date)
    cur.execute('select proxy from %s ;' % table_name)
    proxies = cur.fetchall()
    a = 1
    b = 1
    session_1 = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=5)
    session_1.mount("http://", adapter)
    session_1.mount("https://", adapter)
    for proxy in proxies:
        check_proxy = {
            "http": 'http://' + proxy[0],
            "https": 'https://' + proxy[0]
        }
        print(check_proxy)
        try:
            data = session_1.get(url='https://httpbin.org/get?show_env=1', headers=header, proxies=check_proxy, timeout=2).text
            print('可用%d' % a)
            print(data)#查看代理是否启用
            a += 1
        except:
            print('connect_%s_failed' % table_name)
            print('failed %d' % b)
            b += 1
            sql = 'delete from %s where proxy=\'%s\'; ' % (table_name, proxy[0])
            #   查看语句格式是否正确
            print(sql)
            cur.execute(sql)
            db.commit()


def refreshProxy(url1, url2, url3, url4, url5):
    main(xici=url1, wuyou=url2, kuai=url3, ip66=url4, ip181=url5)


if __name__ == '__main__':

    checkProxy('proxy_wuyou', headers)
    checkProxy('proxy_xici', headers)
    checkProxy('proxy_66', headers)
    checkProxy('proxy_181', headers)
    checkProxy('proxy_kuai', headers)
    checkProxy('proxy_wuyou', headers)
    # refreshProxy()


