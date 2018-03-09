import pymysql
import requests
from db import main
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
}
# 更新数据库


def checkProxy(table_name, header):
    db = pymysql.connect(host='localhost', user='root', password='123456', db='ippools', charset='utf8')
    cur = db.cursor()
    cur.execute('select max(time) from %s' % table_name)
    # 获得最近日期 便于更新时定义待抓取页面
    latest_date = cur.fetchall()
    print(latest_date)
    cur.execute('select proxy from %s' % table_name)
    proxies = cur.fetchall()
    for proxy in proxies:
        #   遍历整张表 删除不可用的代理
        print(proxy[0])
        check_proxy = {'proxy': proxy[0]}
        try:
            requests.get(url='http://www.baidu.com/', headers=header, proxies=check_proxy, timeout=2)
        except:
            print('connect_%s_failed' % table_name)
            cur.execute('delete from %s where proxy=%s' % (table_name, proxy[0]))
        else:
            pass


def refreshProxy(url1, url2, url3, url4, url5):
    #   传入待抓取页面 更新数据库
    main(xici=url1, wuyou=url2, kuai=url3, ip66=url4, ip181=url5)


if __name__ == '__main__':

    checkProxy()
    refreshProxy()


