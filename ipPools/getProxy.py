import requests
from lxml import etree
import pymysql


'''从目标网站获取代理'''


class ProxyCrawl(object):
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
        db = pymysql.connect(host="localhost", user="root", password="123456", db="proxy", charset="utf8")
        cur = db.cursor()
        '''插入代理到主表，备用'''
        sql = 'insert into proxy_main(proxy)values(%s);'
        cur.execute(sql, proxy)
        print('入库成功')
        db.commit()
        db.close()


class Parse(object):

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









