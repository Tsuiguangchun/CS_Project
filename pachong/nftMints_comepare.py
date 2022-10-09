# encoding:utf-8
# @CreateTime: 2022/8/29 20:58
# @Author: Xuguangchun
# @FlieName: nftMints_comepare.py
# @SoftWare: PyCharm


from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import requests


# 爬取gas费
class NftMints:
    def get_html(self, requestUrl):
        User_Agent = UserAgent().random
        html = requests.get(url=requestUrl, headers={"User-Agent": User_Agent})
        print(html.status_code)
        # print(html.text)
        soup = bs(html.text, 'html.parser')
        print(soup)
        return html

    # def get_mints(self):


if __name__ == '__main__':
    nft = NftMints()
    nft.get_html(requestUrl='https://etherscan.io/token/0x8661cd0c4a3fd3dc6b31cd24b20368851749df00#readContract')
