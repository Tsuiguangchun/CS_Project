# encoding:utf-8
# @CreateTime: 2022/8/27 21:45
# @Author: Xuguangchun
# @FlieName: exchange_willList.py
# @SoftWare: PyCharm

import re
import time

from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import requests, random
from common.get_data import *


class NewCoin:
    def __init__(self):
        self.session = requests.Session()
        self.userAgent = UserAgent().random
        self.rw = ReadAndWrite()
        self.pro = self.get_proxy()

    def get_html(self, url):
        soup = None
        proxy = None
        proxy_list = self.rw.load_data(filePath=r'data\ip.yaml')
        if proxy_list is not None:
            proxy_item = random.choice(proxy_list)
            print(proxy_list)
            print(proxy_item)
            proxy = {"https": proxy_item['ip'] + ':' + proxy_item['port']}


            print(proxy)
        else:
            pass
        while True:
            try:
                host = re.match('^(http(s)?:\/\/).*?com|n$',url)
                # if host is not None:
                #
                # print(host)
                headers = {"User-Agent": self.userAgent
                           }
                print(headers)
                status_code = self.session.get(url=url, headers=headers, proxies=proxy).status_code
                print(status_code)
                html = self.session.get(url=url, headers=headers, proxies=proxy).text
                # html = requests.get(url=url, timeout=(3, 30), proxies=random.choice(proxy_list),
                #                     headers={"User-Agent": self.userAgent}).text
                soup = bs(html, 'html.parser')
            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                if 'bad handshake' in str(e) or '10059' in str(e):  # 上述2种异常
                    continue  # 继续发请求
                else:
                    raise Exception(e)  # 其他异常，抛出来
            break
        return soup

    def get_proxy(self):
        self.rw.clear_data(filePath=r'data\ip.yaml')
        url = 'https://www.89ip.cn/'
        soup = self.get_html(url=url)
        tableData = soup.find_all('div', class_='layui-form')
        for i in soup.find_all('tr'):
            str_list = []
            for td in i.find_all('td'):
                td = re.sub('\s|[\u4e00-\u9fa5]', '', td.text)
                str_list.append(td)
                if len(str_list) >= 2:
                    data = str_list[:2]
                    if '' not in data:
                        data = [{"ip": data[0], 'port': data[1]}]
                        self.rw.write_data(filePath=r'data\ip.yaml', needWriteData=data)
                        str_list.clear()
            #     print('=========>>td:',td.text)
            #
            # print('==============>>>>', th)
            # th_data = re.sub('\s', ',', th)
            # ip = i.find('th').text

            # print('==============>>>>', i.text)
            # print('==============>>>>', th_data)
            # print('==============ip>>>>',ip)

        # print("=======>proxy:", i)
        # name1 = soup.select('table>thead>tr')
        # print('=========>',tableData)

    def mexc(self):
        url = 'https://support.mexc.com/hc/en-001/sections/360000547811-New-Listings'
        soup = self.get_html(url=url)
        print("=======>mexc:", soup)

    def huoBi(self):
        url = 'https://www.huobi.com/support/en-us/list/360000039942'
        soup = self.get_html(url=url)
        print("=======>huoBi:", soup)

    def coinsBase(self):
        url = 'https://api.pro.coinbase.com/currencies'
        soup = self.get_html(url=url)
        print("=======>coinsBase:", soup)

    def gateIo(self):
        url = 'https://www.gate.io/articlelist/ann/0  '
        pass

    def okx(self):
        url = 'https://www.okx.com/support/hc/en-us/sections/360000030652-Latest-Announcements'
        pass

    def binance(self):
        url = 'https://www.binance.com/en/support/announcement/c-48?navId=48'
        soup = self.get_html(url=url)
        print("=======>binance:", soup)

    def ftx(self):
        url = 'https://help.ftx.com/hc/en-us/sections/4414741387924-New-Listing-Announcements'
        pass


if __name__ == '__main__':
    newCoin = NewCoin()
    # newCoin.get_html()
    # newCoin.get_proxy()
    newCoin.mexc()
    # newCoin.huoBi()
    # newCoin.binance()
