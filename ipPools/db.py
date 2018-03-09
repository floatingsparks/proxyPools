import pymysql
from getProxy import Proxy
import requests
import time
import random
#   定义待抓取页面
xiCiUrl = ['http://www.xicidaili.com/nn/{}'.format(str(i)) for i in range(1, 16, 1)]
wuYouUrl = ['http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml',
            'http://www.data5u.com/free/gwpt/index.shtml']
url_66 = ['http://www.66ip.cn/{}.html'.format(str(i)) for i in range(1, 16, 1)]
url_181 = ['http://www.ip181.com/daili/{}.html'.format(str(i)) for i in range(1, 16, 1)]
kuaiUrl = ['https://www.kuaidaili.com/free/inha/{}/'.format(str(i)) for i in range(1, 16, 1)]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
}


def xiCiInsert(url, header):
    i = 1
    proxy = Proxy()
    proxies, types, dates = proxy.proxyXiCi(url, header)
    time.sleep(5 + random.randint(2, 9))
    for single_proxy, single_type, date in zip(proxies, types, dates):
        checkproxy = {'proxy': single_proxy}
        try:
            #   检测代理是否可用
            requests.get(url='http://www.baidu.com/', headers=header, proxies=checkproxy, timeout=2)
        except:
            print('xici_connect_failed')
        else:
            #   插入可用代理到对应表
            sql = ''' insert into proxy_xici(time, proxy, type)
                values(%s, %s, %s );'''
            cur.execute(sql, (date, single_proxy, single_type))
            db.commit()
            print('success_xici_%s' % i)
            i += 1


def wuYouInsert(url, header):
    i = 1
    proxy = Proxy()
    proxies, types = proxy.proxyWuYou(url, header)
    time.sleep(5 + random.randint(2, 9))
    for single_proxy, single_type in zip(proxies, types):
        checkproxy = {'proxy': single_proxy}
        try:
            requests.get(url='http://www.baidu.com/', headers=header, proxies=checkproxy, timeout=2)
        except:
            print('wuyou_connect_failed')
        else:
            sql = ''' insert into proxy_wuyou(proxy, type)
            values(%s, %s);'''
            cur.execute(sql, (single_proxy, single_type))
            db.commit()
            print('success_wuyou_%s' % i)
            i += 1


def kuaiInsert(url, header):
    proxy = Proxy()
    i = 1
    proxies, types, dates = proxy.proxyKuaiDaiLi(url, header)
    time.sleep(5 + random.randint(2, 9))
    for single_proxy, single_type, date in zip(proxies, types, dates):
        checkproxy = {'proxy': single_proxy}
        try:
            requests.get(url='http://www.baidu.com/', headers=header, proxies=checkproxy, timeout=2)
        except:
            print('kuai_connect_failed')
        else:
            sql = ''' insert into proxy_kuai(time, proxy, type)
            values(%s, %s, %s );'''
            cur.execute(sql, (date, single_proxy, single_type))
            db.commit()
            print('success_kuai_%s' % i)
            i += 1


def proxy66Insert(url, header):
    proxy = Proxy()
    i = 1
    proxies, dates = proxy.proxy_66(url, header)
    time.sleep(5 + random.randint(2, 9))
    for single_proxy, date in zip(proxies, dates):
        checkproxy = {'proxy': single_proxy}
        try:
            requests.get(url='http://www.baidu.com/', headers=header, proxies=checkproxy, timeout=2)
        except:
            print('connect_66_failed')
        else:
            sql = ''' insert into proxy_66(time, proxy)
            values(%s, %s);'''
            cur.execute(sql, (date, single_proxy))
            db.commit()
            print('success_66_%s' % i)
            i += 1


def proxy181Insert(url, header):
    proxy = Proxy()
    i = 1
    proxies, types, dates = proxy.proxy_181(url, header)
    time.sleep(5 + random.randint(2, 9))
    for single_proxy, single_type, date in zip(proxies, types, dates):
        checkproxy = {'proxy': single_proxy}
        try:
            requests.get(url='http://www.baidu.com/', headers=header, proxies=checkproxy, timeout=2)
        except:
            print('connect_181_failed')
        else:
            sql = ''' insert into proxy_181(time, proxy, type)
            values(%s, %s, %s );'''
            cur.execute(sql, (date, single_proxy, single_type))
            db.commit()
            print('success_181_%s' % i)
            i += 1


def main(xici, wuyou, kuai, ip66, ip181):
    for url in xici:
        xiCiInsert(url, headers)
    for url in wuyou:
        wuYouInsert(url, headers)
    for url in kuai:
        kuaiInsert(url, headers)
    for url in ip66:
        proxy66Insert(url, headers)
    for url in ip181:
        proxy181Insert(url, headers)


if __name__ == '__main__':
    db = pymysql.connect(host="localhost", user="root", password="123456", db="ippools", charset="utf8")
    cur = db.cursor()
    main(xiCiUrl, wuYouUrl, kuaiUrl, url_66, url_181)
    db.close()