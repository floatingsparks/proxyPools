import pymysql
from getProxy import Proxy
import requests
from requests.adapters import HTTPAdapter
import time
import random
xiCiUrl = ['http://www.xicidaili.com/nn/{}'.format(str(i)) for i in range(1, 55, 1)]
wuYouUrl = ['http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml',
            'http://www.data5u.com/free/gwpt/index.shtml']
url_66 = ['http://www.66ip.cn/{}.html'.format(str(i)) for i in range(1, 55, 1)]
url_181 = ['http://www.ip181.com/daili/{}.html'.format(str(i)) for i in range(1, 55, 1)]
kuaiUrl = ['https://www.kuaidaili.com/free/inha/{}/'.format(str(i)) for i in range(1, 55, 1)]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
}


def xiCiInsert(url, header):
    proxy = Proxy()
    proxies, types, dates = proxy.proxyXiCi(url, header)
    #   设置最大请求次数
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=2)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    for single_proxy, single_type, date in zip(proxies, types, dates):
        check_proxy = {
            'http': 'http://' + single_proxy,
            'https': 'https://' + single_proxy
        }
        try:
            #   验证代理是否可用
            session.get(url='http://sz.58.com/chuzu/pn1/', headers=header, proxies=check_proxy, timeout=3)
        except:
            print('xici_connect_failed')
        else:
            sql = ''' insert into proxy_xici(time, proxy, type)
                values(%s, %s, %s );'''
            cur.execute(sql, (date, single_proxy, single_type))
            db.commit()
            print('success_xici')
            


def wuYouInsert(url, header):
    proxy = Proxy()
    proxies, types = proxy.proxyWuYou(url, header)
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=2)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    for single_proxy, single_type in zip(proxies, types):
        check_proxy = {
            'http': 'http://' + single_proxy,
            'https': 'https://' + single_proxy
        }
        print(check_proxy)
        try:
            session.get(url='http://sz.58.com/chuzu/pn1/', headers=header, proxies=check_proxy, timeout=3)
        except:
            print('wuyou_connect_failed')
        else:
            sql = ''' insert into proxy_wuyou(proxy, type)
            values(%s, %s);'''
            cur.execute(sql, (single_proxy, single_type))
            db.commit()
            print('success_wuyou')
            


def kuaiInsert(url, header):
    proxy = Proxy()
    proxies, types, dates = proxy.proxyKuaiDaiLi(url, header)
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=2)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    for single_proxy, single_type, date in zip(proxies, types, dates):
        check_proxy = {
            'http': 'http://' + single_proxy,
            'https': 'https://' + single_proxy
        }
        try:
            session.get(url='http://sz.58.com/chuzu/pn1/', headers=header, proxies=check_proxy, timeout=3)
        except:
            print('kuai_connect_failed')
        else:
            sql = ''' insert into proxy_kuai(time, proxy, type)
            values(%s, %s, %s );'''
            cur.execute(sql, (date, single_proxy, single_type))
            db.commit()
            print('success_kuai')
            


def proxy66Insert(url, header):
    proxy = Proxy()
    proxies, dates = proxy.proxy_66(url, header)
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=2)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    for single_proxy, date in zip(proxies, dates):
        check_proxy = {
            'http': 'http://' + single_proxy,
            'https': 'https://' + single_proxy
        }
        try:
            session.get(url='http://sz.58.com/chuzu/pn1/', headers=header, proxies=check_proxy, timeout=3)
        except:
            print('connect_66_failed')
        else:
            sql = ''' insert into proxy_66(time, proxy)
            values(%s, %s);'''
            cur.execute(sql, (date, single_proxy))
            db.commit()
            print('success_66')
            


def proxy181Insert(url, header):
    proxy = Proxy()
    proxies, types, dates = proxy.proxy_181(url, header)
	# 设置最大请求次数
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=2)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    for single_proxy, single_type, date in zip(proxies, types, dates):
        check_proxy = {
            'http': 'http://' + single_proxy,
            'https': 'https://' + single_proxy
        }
        try:
            session.get(url='http://sz.58.com/chuzu/pn1/', headers=header, proxies=check_proxy, timeout=3)
        except:
            print('connect_181_failed')
        else:
            sql = ''' insert into proxy_181(time, proxy, type)
            values(%s, %s, %s );'''
            cur.execute(sql, (date, single_proxy, single_type))
            db.commit()
            print('success_181')
            


def main(wuyou, xici, kuai, ip66, ip181):
    for url in wuyou:
        print('=================================')
        time.sleep(random.randint(2, 5))
        wuYouInsert(url, headers)
    for url in xici:
        time.sleep(random.randint(2, 5))
        xiCiInsert(url, headers)
    for url in kuai:
        time.sleep(random.randint(2, 5))
        kuaiInsert(url, headers)
    for url in ip66:
        time.sleep(random.randint(2, 5))
        proxy66Insert(url, headers)
    for url in ip181:
        time.sleep(random.randint(2, 5))
        proxy181Insert(url, headers)


if __name__ == '__main__':
    db = pymysql.connect(host="localhost", user="root", password="123456", db="ippools", charset="utf8")
    cur = db.cursor()
    main(wuYouUrl, xiCiUrl, kuaiUrl, url_66, url_181)
    db.close()



