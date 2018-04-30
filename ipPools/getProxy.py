import requests
from lxml import etree
import pymysql


class ProxyCrawl(object):
	'''爬取代理并储存'''
    def __init__(self,):
        pass

    def proxyGet(self, url, header, parse):
        try:
            response = requests.get(url=url, headers=header).content
            selector = etree.HTML(response)
            ips, ports = parse(selector)
            info = self.proxy(ips, ports)
            while True:
                self.insertTodb(next(info))
        except Exception as e:
            print(e)

    @staticmethod
    def proxy(ips, ports):
        '''使用生成器'''
        for ip, port in zip(ips, ports):
            info = ip + ':' + port
            yield info

    @staticmethod
    def insertTodb(proxy):
        '''插入数据到mysql'''
        db = pymysql.connect(host="localhost", user="root", password="1992825", db="proxy", charset="utf8")
        cur = db.cursor()
        sql = 'insert into proxy(proxy)values(%s);'
        # lock = Lock()
        # lock.acquire()
        cur.execute(sql, proxy)
        # lock.release()
        print('插入成功')
        db.commit()
        db.close()


class Parse(object):
	'''解析方法'''
    def __init__(self, ):
        pass

    @staticmethod
    def parseXiCI(selector):
        ips = selector.xpath('//tr[@class="odd"]/td[2]/text()')
        ports = selector.xpath('//tr[@class="odd"]/td[3]/text()')
        return ips, ports

    @staticmethod
    def parseWuYou(selector):
        ips = selector.xpath('//li[@style="text-align:center;"]/ul[position()>1]/span[1]/li/text()')
        ports = selector.xpath('//li[@style="text-align:center;"]/ul[position()>1]/span[2]/li/text()')
        return ips, ports

    @staticmethod
    def parse66(selector):
        ips = selector.xpath('//div[@id="main"]/div/div[1]/table/tr[position()>1]/td[1]/text()')
        ports = selector.xpath('//div[@id="main"]/div/div[1]/table/tr[position()>1]/td[2]/text()')
        return ips, ports

    @staticmethod
    def parseKuaiDaiLi(selector):
        ips = selector.xpath('//div[@id="list"]/table/tbody/tr/td[1]/text()')
        ports = selector.xpath('//div[@id="list"]/table/tbody/tr/td[2]/text()')
        return ips, ports










