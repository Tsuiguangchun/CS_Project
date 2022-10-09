# encoding:utf-8
# @CreateTime: 2022/7/25 18:02
# @Author: Xuguangchun
# @FlieName: get_accessToken.py
# @SoftWare: PyCharm
import datetime

from common.requestMethod import *
from common.rsa_encode import *
from common.get_environment import *
from common.log import *
from common.get_data import *
import time
import re
from pachong.gas_compare import *
from common.sendMsg_DingTalk import *

"""

# 根据POM设置模式进行代码封装
# api业务解析
# HomePage基类(初始化环境配置)
# 判断令牌有效期内不再调用请求生成新令牌
"""


# 执行之前需要清除的旧数据，可以写到用例setup()里面或者conftest.py 文件fixture夹具中
def clear_fileData(clear_filepath):
    delete = ReadAndWrite()
    for file in clear_filepath:
        delete.clear_data(file)


need_clear_filepath = [
    'data\\priceChart_error.yaml',
    'data\\marketChart_error.yaml',
    'data\\result_IsEmpty.yaml',
    'data\\request_Fail.yaml',
    'data\\responseTime_Over3s.yaml',
    'data\\coinMarkers_chart_duration.yaml',
    'data\\coinsPrice_chart_duration.yaml',
    'data\\getDexInfo.yaml'

]
clear_fileData(clear_filepath=need_clear_filepath)


class HomePage:
    def __init__(self, env, urlFile, apiVersion, app_version):
        self.send = Send_api(env=env, apiVersion=apiVersion, app_version=app_version)
        self.app_key = self.send.app_key
        self.secret = self.send.secret
        self.logger = CSLog()
        self.ReadAndWrite = ReadAndWrite()
        self.url_file = self.ReadAndWrite.load_data(urlFile)  # 所有url地址都在同一个yaml文件内
        self.api_version = apiVersion
        self.dingTalk = DingTalk()

    # 获取访问令牌token
    def get_accessToken(self):
        tokenPath = r"D:\cs_project\data\token.yaml"
        check_token = self.ReadAndWrite.load_data(tokenPath)
        url = self.url_file["initApi"]["getToken"]
        data = self.ReadAndWrite.load_data("data\\bodyData.yaml")['get_token']
        if os.path.exists(tokenPath) and self.ReadAndWrite.load_data(filePath=tokenPath) is not None:
            if int(time.time()) <= check_token['expire_time']:
                Token = check_token['access-token']
                self.send.baseHeaders.update({'access-token': Token})
            else:
                self.ReadAndWrite.clear_data(tokenPath)
                data.update({"app_key": self.app_key, "secret": rsa_encrypt(self.secret)})
                self.send.main_request(methods="POST", url=url, data=data)
        else:
            self.ReadAndWrite.clear_data(tokenPath)
            data.update({"app_key": self.app_key, "secret": rsa_encrypt(self.secret)})
            self.send.main_request(methods="POST", url=url, data=data)

    # 首页工具
    def get_tools_list(self):
        url = self.url_file['initApi']["getToolsList"]
        self.send.main_request("GET", url=url)

    # 热门搜索合约
    def get_HotSearchContract(self):
        url = self.url_file['initApi']["getHotSearchContract"]
        self.send.main_request("GET", url=url)

    # 合约搜索
    def queryContract(self):
        url = self.url_file['initApi']["queryContract"]
        self.send.main_request("GET", url=url)

    # 市场数据
    def get_MarketIndexList(self):
        self.logger.log("=======市场数据接口开始请求=======")
        url = self.url_file['initApi']["getMarketIndexList"]
        self.send.main_request("GET", url=url)

    # 发现页
    def getDiscoverCoinList(self):
        url = self.url_file['discover']["getDiscoverCoinList"]
        self.send.main_request("GET", url=url)

    # 我的模块动态入口栏
    def get_UserRecommendToolbar(self):
        url = self.url_file['initApi']["getUserRecommendToolbar"]
        self.send.main_request(methods="GET", url=url)

    # 法定货币单价
    def get_CurrencyCodeList(self):
        self.logger.log("=========货币接口开始请求=========")
        url = self.url_file['initApi']["getCurrencyCodeList"]
        self.send.main_request(methods="GET", url=url)

    # 公链配置
    def get_chainSetting(self):
        url = self.url_file['tools']['getGasChainSetting']
        response = self.send.main_request(methods="GET", url=url)
        return response['result'][0]['chain']

    # gas 跟踪
    def get_gas(self):
        self.ReadAndWrite.clear_data(filePath=r'data\gasReport.yaml')
        url = self.url_file['tools']['gasTracker']
        chain = self.get_chainSetting()
        response = self.send.main_request(methods="GET", url=url, params={'chain': chain})
        result = response['result']

        if len(result) != 0:
            compare_data = Gas().get_gas_info()
            eth_data = compare_data
            time.sleep(3)
            gas_level = ['low', 'avg', 'high']

            compare_false = 0
            for i in gas_level:
                if result[i + '_gas_price'] == eth_data[i]['gas'] and \
                        result[i + '_gas_price_usd'] == eth_data[i]['price'] and \
                        result[i + '_confirmation_duration'] == eth_data[i]['confirm_time']:
                    self.ReadAndWrite.write_data(filePath=r"data\gasReport.yaml", needWriteData="校验成功")
                    return self.logger.log('gas 校验成功')
                else:
                    self.ReadAndWrite.write_data(filePath=r"data\gasReport.yaml", needWriteData="校验配对不一致")
                    return self.logger.log('gas 校验失败')
        else:
            self.ReadAndWrite.write_data(filePath=r"data\gasReport.yaml", needWriteData="无数据校验")
            return self.logger.log('无数据校验')

    def get_nft_track(self):
        self.ReadAndWrite.clear_data(filePath=r'data\nftTracker_Info.yaml')
        url = self.url_file['tools']['getNftList']
        data = self.ReadAndWrite.load_data(filePath=r'data\nftTracker_list.yaml')
        for mints in range(len(data)):
            time_type = data[mints]['time_type']
            response = self.send.main_request("GET", url=url, params=data[mints])
            result = response['result']
            for mint in result['list']:
                max_supply = mint['max_supply']
                total_supply = mint['total_supply']
                _data = [{"marketplace": mint['marketplace'],
                          "address": mint['address'],
                          "time_type": time_type}]
                self.ReadAndWrite.write_data(filePath=r'data\nftTracker_Info.yaml', needWriteData=_data)
                if -1 <= total_supply <= 0:
                    _name = [{"name": mint['name'],
                              "address": mint['address'],
                              "total_supply": total_supply}]
                    self.dingTalk.errorLog_sending(logData="NFT mints列表总供应数量异常:\n触发时间：{}\n位置：{}\n异常描述：{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data['time_type'], _name))
                    self.ReadAndWrite.write_data(filePath=r'data\errorMintsSupply.yaml', needWriteData=_name)

                else:
                    pass

    def get_nft_info(self, nftTracker_Info):
        url = self.url_file['tools']['getNftInfo']
        # _data = ReadAndWrite().load_data(filePath=r'data\nftTracker_Info.yaml')
        result = self.send.main_request(methods="GET", url=url, params=nftTracker_Info)['result']
        time_type = nftTracker_Info['time_type']
        if int(result['max_supply']) > 0 and result['max_supply'] < int(result['mints']['count']):
            self.dingTalk.errorLog_sending(logData="mints 总铸造量大于最大供应量值：\n触发时间:{}"
                                                   "\n采集后统计总mints值：{} > 最大供应量值：{}"
                                                   "\n名称：{}\n合约地址：{},\n位置: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(result['mints']['count']), result['max_supply'],result['name'], result['address'], time_type))
        else:
            pass

        time_list = ['past_5m', 'past_30m', 'past_1h', 'past_24h', 'count']
        for t in time_list:
            if int(result['makers'][t]) > int(result['mints'][t]):
                self.dingTalk.errorLog_sending(logData="{}区间范围内铸造者大于mints铸造数量：\n触发时间:{}"
                                                       "\n铸造者数量：{} > mints数量：{}"
                                                       "\n名称：{}\n合约地址：{}\n位置：{}".format(time_type, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(result['makers'][t]), int(result['mints'][t]), result['name'], result['address'], t))
            else:
                pass


# if __name__ == '__main__':
#     T = HomePage(env="releaseEnvironment", urlFile="data\\api.yaml", apiVersion="v1_2_0", app_version='1.4.1')
#     T.get_accessToken()
#     T.get_nft_track()
# T.get_cexList()
#     T.get_tools_list()
# T.get_HotSearchContract()
# T.getDiscoverCoinList()
# T.queryContract()
# T.get_MarketIndexList()
# T.get_UserRecommendToolbar()
# T.get_CurrencyCodeList()

# T.get_cexCoinInfo(cexCoinInfo={
#     "coin_id": "xrp"
#     # "exchange": "binance",
#     # "symbol": "BTC"
#     })
