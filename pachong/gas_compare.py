# encoding:utf-8
# @CreateTime: 2022/8/29 15:52
# @Author: Xuguangchun
# @FlieName: gas_compare.py
# @SoftWare: PyCharm

import re

from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import requests


# 爬取gas费
class Gas:
    def get_html(self, requestUrl):
        User_Agent = UserAgent().random
        html = requests.get(url=requestUrl, headers={"User-Agent": User_Agent}).text
        return html

    def get_gas_info(self):
        url = 'https://etherscan.io/gastracker'
        soup = bs(self.get_html(requestUrl=url), 'html.parser')
        low_data = {}
        avg_data = {}
        high_data = {}
        gas_info = {
            "low": low_data,
            "avg": avg_data,
            "high": high_data
        }

        def gas_level_time(secondary_list, need_update_data):

            if ':' in secondary_list[1]:
                time = re.sub('~|mins|secs', '', secondary_list[1])
                time_list = time.split(':')
                minute = int(time_list[0])
                second = int(time_list[1])
                confirm_time = minute * 60 + second
                need_update_data.update({"confirm_time": confirm_time})
                # need_update_data.update({"minute": minute, "second": second})
                # print('low_minute:=================>', low_minute)
                # print('low_second:=================>', low_second)
            else:
                if 'mins' in secondary_list[1]:
                    minute = int(re.sub('~|mins', '', secondary_list[1]))
                    confirm_time = minute * 60
                    need_update_data.update({"confirm_time": confirm_time})
                    # print('low_minute:=================>', low_minute)
                else:
                    second = int(re.sub('~|secs', '', secondary_list[1]))
                    need_update_data.update({"confirm_time": second})
                    # print('low_second:=================>', low_second)

        for card in soup.find_all('div', class_='card h-100 shadow-none p-3'):
            print("================================分割线====================================")
            if card.find('div', id='divLowPrice'):
                secondary_list = card.find_all_next('div', class_='text-secondary')[1].text.split('|')
                low_gas = int(card.find('span', id='spanLowPrice').text)
                low_price = float(re.sub('[$]', '', secondary_list[0]))
                low_data.update({"gas": low_gas, "price": low_price})
                gas_level_time(secondary_list=secondary_list, need_update_data=low_data)

            elif card.find('div', id='divAvgPrice'):
                secondary_list = card.find_all_next('div', class_='text-secondary')[1].text.split('|')
                avg_gas = int(card.find('span', id='spanAvgPrice').text)
                avg_price = float(re.sub('[$]', '', secondary_list[0]))
                avg_data.update({"gas": avg_gas, "price": avg_price})
                gas_level_time(secondary_list=secondary_list, need_update_data=avg_data)

            elif card.find('div', id='divHighPrice'):
                secondary_list = card.find_all_next('div', class_='text-secondary')[1].text.split('|')
                high_gas = int(card.find('span', id='spanHighPrice').text)
                high_price = float(re.sub('[$]', '', secondary_list[0]))
                high_data.update({"gas": high_gas, "price": high_price})
                gas_level_time(secondary_list=secondary_list, need_update_data=high_data)

        # print("低速：", low_data)
        # print("中速：", avg_data)
        # print("高速：", high_data)
        # print('gasInfo', gas_info)
        print(gas_info)

        return gas_info


if __name__ == '__main__':
    Gas().get_gas_info()
