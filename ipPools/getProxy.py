import requests
from lxml import etree
from bs4 import BeautifulSoup


class Proxy(object):

        def __init__(self):
            pass

        def proxyXiCi(self, url, header):
            #   抓取西刺代理 http://www.xicidaili.com
            proxy = []
            try:
                response = requests.get(url=url, headers=header).content
            except:
                print('xici_crawl_failed')
            else:
                selector = etree.HTML(response)
                ips = selector.xpath('//tr[@class="odd"]/td[2]/text()')
                ports = selector.xpath('//tr[@class="odd"]/td[3]/text()')
                types = selector.xpath('//tr[@class="odd"]/td[6]/text()')
                time = selector.xpath('//tr[@class="odd"]/td[10]/text()')
                for ip, port in zip(ips, ports):
                    #   组合ip和端口
                    info = ip + ':' + port
                    proxy.append(info)
                return proxy, types, time

        def proxyWuYou(self, url, header):
            #   抓取5u代理 http://www.data5u.com
            proxy = []
            try:
                response = requests.get(url=url, headers=header).text
            except:
                print('wuyou_crawl_failed')
            else:
                selector = BeautifulSoup(response, 'lxml')
                ips = selector.select('ul[class="l2"] > span:nth-of-type(1) > li')
                ports = selector.select('ul[class="l2"] > span:nth-of-type(2) > li')
                types = selector.select('ul[class="l2"] > span:nth-of-type(4) > li > a')
                real_type = []
                for ip, port, single_type in zip(ips, ports, types):
                    info = ip.get_text() + ':' + port.get_text()
                    info1 = single_type.get_text()
                    proxy.append(info)
                    real_type.append(info1)
                return proxy, real_type

        def proxy_66(self, url, header):
            #   抓取66代理 http://www.66ip.cn
            proxy = []
            try:
                response = requests.get(url=url, headers=header).content
            except:
                print('crawl_66_failed')
            else:
                selector = etree.HTML(response)
                ips = selector.xpath('//div[@id="main"]/div/div[1]/table/tr[position()>1]/td[1]/text()')
                ports = selector.xpath('//div[@id="main"]/div/div[1]/table/tr[position()>1]/td[2]/text()')
                time = selector.xpath('//div[@id="main"]/div/div[1]/table/tr[position()>1]/td[5]/text()')
                info = []
                #   数据规整
                for i in time:
                    i = i[:-3]
                    info.append(i)
                time = info
                for ip, port in zip(ips, ports):
                    info = ip + ':' + port
                    proxy.append(info)
                return proxy, time

        def proxy_181(self, url, header):
            #   抓取181代理 http://www.ip181.com
            proxy = []
            try:
                response = requests.get(url=url, headers=header).content
            except:
                print('crawl_181_failed')
            else:
                selector = etree.HTML(response)
                ips = selector.xpath('//table/tbody/tr[position()>1]/td[1]/text()')
                ports = selector.xpath('//table/tbody/tr[position()>1]/td[2]/text()')
                types = selector.xpath('//table/tbody/tr[position()>1]/td[4]/text()')
                time = selector.xpath('//table/tbody/tr[position()>1]/td[7]/text()')
                for ip, port in zip(ips, ports):
                    info = ip + ':' + port
                    proxy.append(info)
                return proxy, types, time

        def proxyKuaiDaiLi(self, url, header):
            #   抓取kuaidaili https://www.kuaidaili.com
            proxy = []
            try:
                response = requests.get(url=url, headers=header).content
            except:
                print('kuaiDaiLi_crawl_failed')
            else:
                selector = etree.HTML(response)
                ips = selector.xpath('//div[@id="list"]/table/tbody/tr/td[1]/text()')
                ports = selector.xpath('//div[@id="list"]/table/tbody/tr/td[2]/text()')
                types = selector.xpath('//div[@id="list"]/table/tbody/tr/td[4]/text()')
                time = selector.xpath('//div[@id="list"]/table/tbody/tr/td[7]/text()')
                for ip, port in zip(ips, ports):
                    info = ip + ':' + port
                    proxy.append(info)
                return proxy, types, time
