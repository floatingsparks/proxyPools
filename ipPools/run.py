from multiprocessing import Pool
import pymysql
import multiprocessing
from getProxy import ProxyCrawl, Parse
import threading
from refresh import RefreshProxy
import time

'''可执行文件'''

xiCiUrl = ['http://www.xicidaili.com/nn/{}'.format(str(i)) for i in range(1, 300, 1)]
url_66 = ['http://www.66ip.cn/{}.html'.format(str(i)) for i in range(1, 300, 1)]
kuaiUrl = ['https://www.kuaidaili.com/free/inha/{}/'.format(str(i)) for i in range(1, 300, 1)]
wuYouUrl = ['http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml',
            'http://www.data5u.com/free/gwpt/index.shtml']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate'
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
            time.sleep(1)
    p.close()
    p.join()


def multi_check(header):
    '''高并发检测可用代理'''
    db = pymysql.connect(host="localhost", user="root", password="123456", db="proxy", charset="utf8")
    cur = db.cursor()
    sql = "select proxy from proxy_main;"
    cur.execute(sql)
    db.commit()
    '''获取所有代理'''
    proxy = cur.fetchall()
    sql1 = "truncate proxy_dingdianxiaoshuo"
    cur.execute(sql1)
    db.commit()
    db.close()
    p = Pool(100)
    for single_proxy in proxy:
        refresh = RefreshProxy(header)
        p.apply_async(refresh.check, args=(single_proxy, ))
    p.close()
    p.join()


if __name__ == '__main__':
    '''爬取代理并储存'''
    parse = Parse()
    list_thread = []
    t1 = threading.Thread(target=multi_get, args=(xiCiUrl, headers,  parse.parseXiCI))
    t2 = threading.Thread(target=multi_get, args=(wuYouUrl, headers, parse.parseWuYou))
    t3 = threading.Thread(target=multi_get, args=(url_66, headers, parse.parse66))
    t4 = threading.Thread(target=multi_get, args=(kuaiUrl, headers, parse.parseKuaiDaiLi))
    list_thread = [t1, t2, t3, t4]
    for thread in list_thread:
        thread.start()
    for thread in list_thread:
        thread.join()
    '''检测可用代理'''
    print("开始检测")
    multi_check(headers)






