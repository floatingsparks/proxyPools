from multiprocessing import Pool
import pymysql
import multiprocessing
from getProxy import ProxyCrawl, Parse
import threading
from refresh import RefreshProxy
import os
xiCiUrl = ['http://www.xicidaili.com/nn/{}'.format(str(i)) for i in range(1, 70, 1)]
url_66 = ['http://www.66ip.cn/{}.html'.format(str(i)) for i in range(1, 80, 1)]
kuaiUrl = ['https://www.kuaidaili.com/free/inha/{}/'.format(str(i)) for i in range(1, 70, 1)]
wuYouUrl = ['http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml',
            'http://www.data5u.com/free/gwpt/index.shtml']

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
}


def multi_get(urls, header, parse):
    '''多进程爬取代理并存入mysql'''
    p = Pool(multiprocessing.cpu_count())
    loaded = []
    for url in urls:
        '''判断链接是否已经爬取'''
        if url in loaded:
            pass
        else:
            '''调用proxyGet进行爬取'''
            proxy = ProxyCrawl()
            p.apply_async(proxy.proxyGet, args=(url, header, parse))
            '''保存已爬取的链接'''
            loaded.append(url)
    p.close()
    p.join()


def multi_check(header):
    '''高并发检测mysql中的代理'''
    print("run fa %s" % (os.getpid()))
    db = pymysql.connect(host="localhost", user="root", password="123456", db="proxy", charset="utf8")
    cur = db.cursor()
    sql = "select proxy from proxy;"
    cur.execute(sql)
    db.commit()
    '''获取所有代理'''
    proxy = cur.fetchall()
    sql = "truncate proxy;"
    cur.execute(sql)
    db.commit()
    p = Pool(100)
    for single_proxy in proxy:
        refresh = RefreshProxy(header)
        p.apply_async(refresh.check, args=(single_proxy, ))
    p.close()
    p.join()


if __name__ == '__main__':
    '''爬取代理并储存'''
    parse = Parse()
    threading.Thread(target=multi_get, args=(xiCiUrl, headers,  parse.parseXiCI)).start()
    threading.Thread(target=multi_get, args=(wuYouUrl, headers, parse.parseWuYou)).start()
    threading.Thread(target=multi_get, args=(url_66, headers, parse.parse66)).start()
    threading.Thread(target=multi_get, args=(kuaiUrl, headers, parse.parseKuaiDaiLi)).start()
    '''检测代理可用性'''
    multi_check(headers)






