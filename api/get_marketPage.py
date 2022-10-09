# encoding:utf-8
# @CreateTime: 2022/8/2 10:48
# @Author: Xuguangchun
# @FlieName: get_marketPage.py
# @SoftWare: PyCharm

from common.requestMethod import *
from common.rsa_encode import *
from common.get_environment import *
from common.log import *
from common.get_data import *
from common.get_pageNo import *
from api.get_homePage import *


class MarketsPage(HomePage):

    # cex货币列表
    def get_cexList(self, pageSize, one=True):
        self.ReadAndWrite.clear_data(filePath=r'data\\getCexInfo.yaml', headline=True,
                                     needWriteData=[
                                         {'coin_id': 'bitcoin', 'exchange': 'binance', 'symbol': 'BTC', 'day': 1}])

        url = self.url_file['markets']["getCexList"]

        def explain_response(responseData):
            error_priceList = []

            for coinInfo in responseData['result']['items']:
                if 'coin_id' and 'exchange' and 'symbol' in coinInfo and coinInfo['data_source'] == 'cex':
                    _data = [{'coin_id': coinInfo['coin_id'],
                              'exchange': coinInfo['exchange'],
                              'symbol': coinInfo['symbol'],
                              'day': 1}]
                    # print("=======》currentData:", data)
                    self.ReadAndWrite.write_data(filePath=r'data\\getCexInfo.yaml', needWriteData=_data)

                elif 'coin_id' and 'exchange' and 'symbol' in coinInfo and coinInfo['data_source'] == 'dex':
                    _data = [{'coin_id': coinInfo['coin_id'],
                              'exchange': coinInfo['exchange'],
                              'symbol': coinInfo['symbol'],
                              'day': 1}]
                    self.ReadAndWrite.write_data(filePath=r'data\\getDexInfo.yaml', needWriteData=_data)

                else:
                    continue

                if float(coinInfo['price']) <= 0:
                    symbolPrice_error = coinInfo['symbol']
                    error_priceList.append(symbolPrice_error)
                    self.ReadAndWrite.write_data(filePath=r'data\symbolPrice_error.yaml', needWriteData=error_priceList)
                else:
                    pass

        if one:
            pageNum = {"page_size": pageSize, "page_no": 1}
            response = self.send.main_request(methods="GET", url=url, params=pageNum)
            explain_response(responseData=response)

        else:
            response = self.send.main_request(methods="GET", url=url)
            total = response['result']['paging']['total']
            # print("=======》currentTotal:", total)
            pageList = get_pageNo(totalNum=total, pageSize=pageSize)
            for page in pageList:
                response = self.send.main_request(methods="GET", url=url, params=page)
                explain_response(responseData=response)

                # 将货币详情接口参数提取写入到驱动文件内,封装成内部函数减少代码耦合
                # coinList = []
                priceErrorList = []

                # for coinInfo in response['result']['items']:
                #     if 'coin_id' and 'exchange' and 'symbol' in coinInfo:
                #         data = [{'coin_id': coinInfo['coin_id'],
                #                  'exchange': coinInfo['exchange'],
                #                  'symbol': coinInfo['symbol']}]
                #         # print("=======》currentData:", data)
                #         self.ReadAndWrite.write_data(filePath=r'data\\getCexInfo.yaml', needWriteData=data)
                #     else:
                #         continue
                #
                #     if float(coinInfo['price']) <= 0:
                #         symbolPrice_error = coinInfo['symbol']
                #         priceErrorList.append(symbolPrice_error)
                #         self.ReadAndWrite.write_data(filePath=r'data\symbolPrice_error.yaml',
                #                                      needWriteData=priceErrorList)
                #     else:
                #         pass

    # cex货币详情
    def get_cexCoinInfo(self, cexCoinInfo):
        url = self.url_file['markets']["getTokenCexDataInfo"]
        self.send.main_request(methods="POST", url=url, data=cexCoinInfo)
        time.sleep(1)

    # cex 货币详情价格趋势图数据
    # 轮询各个区间步长，比较间隔是否缺数据并记录跳出当前循环

    def get_cexCoinChart(self, cexCoinInfo):
        # self.ReadAndWrite.clear_data(filePath=r'data\\priceChart_error.yaml')
        url = self.url_file['markets']["getTokenCexLineChart"]
        symbol = cexCoinInfo['symbol']
        duration = None
        expect_num = None
        day = [1, 7, 30, 90, 365]
        for days in day:
            cexCoinInfo.update({'day': days})
            if days == 1:
                duration = 300
                expect_num = 288
            elif days == 7:
                duration = 1800
                expect_num = 336
            elif days == 30:
                duration = 14400
                expect_num = 180
            elif days == 90:
                duration = 14400
                expect_num = 540
            elif days == 365:
                duration = 86400
                expect_num = 365

            response = self.send.main_request(methods="GET", url=url, params=cexCoinInfo)
            if len(response['result']['list']) <= 2 or len(response['result']) == 0:
                _data = [cexCoinInfo['symbol']]
                self.ReadAndWrite.write_data(filePath=r'data\\priceChart_error.yaml', needWriteData=_data)
            else:
                pass

            if len(response['result']['list']) >= 3:
                for t in range(len(response['result']['list']) - 1):
                    t2 = t + 1

                    next_time = int(response['result']['list'][t2]['time'])
                    last_time = int(response['result']['list'][t]['time'])
                    if next_time - last_time != duration:
                        error_duration = [{"symbol": symbol, "day": days, "count_num": len(response["result"]["list"]),
                                           "expect_num": expect_num, "exception_duration": (last_time, next_time)}]
                        self.ReadAndWrite.write_data(filePath=r'data\coinsPrice_chart_duration.yaml',
                                                     needWriteData=error_duration)
                        # self.dingTalk.errorLog_sending(
                        #     logData='{}近{}天价格趋势图共有{}点，期望{}个点，步长间隔异常：\n触发时间：{}\n位置：{}'.format(symbol, days, len(
                        #         response["result"]["list"]), expect_num, datetime.datetime.now().strftime(
                        #         "%Y-%m-%d %H:%M:%S"), (last_time, next_time)))

                        break
                    else:
                        pass
            else:
                pass

    # cex 货币详情市值趋势图数据
    def get_MarketCapChart(self, cexCoinInfo):
        url = self.url_file['markets']["getTokenCexMarketCapChart"]
        symbol = cexCoinInfo['symbol']
        duration = None
        expect_num = None
        day = [1, 7, 30, 90, 365]
        for days in day:
            cexCoinInfo.update({'day': days})
            if days == 1:
                duration = 300
                expect_num = 288
            elif days == 7:
                duration = 1800
                expect_num = 336
            elif days == 30:
                duration = 14400
                expect_num = 180
            elif days == 90:
                duration = 14400
                expect_num = 540
            elif days == 365:
                duration = 86400
                expect_num = 365

            # self.ReadAndWrite.clear_data(filePath=r'data\\marketChart_error.yaml')

            response = self.send.main_request(methods="GET", url=url, params=cexCoinInfo)
            if len(response['result']) == 0 or len(response['result']['list']) <= 2:
                _data = [cexCoinInfo['symbol']]
                self.ReadAndWrite.write_data(filePath=r'data\\marketChart_error.yaml', needWriteData=_data)
            else:
                pass
            if len(response['result']['list']) >= 3:
                for t in range(len(response['result']['list']) - 1):
                    t2 = t + 1
                    next_time = int(response['result']['list'][t2]['time'])
                    last_time = int(response['result']['list'][t]['time'])
                    if next_time - last_time != duration:
                        error_duration = [{"symbol": symbol, "day": days, "count_num": len(response["result"]["list"]),
                                           "expect_num": expect_num, "exception_duration": (last_time, next_time)}]
                        self.ReadAndWrite.write_data(filePath=r'data\coinMarkers_chart_duration.yaml',
                                                     needWriteData=error_duration)
                        # self.dingTalk.errorLog_sending(
                        #     logData='{}近{}天市值趋势图共有{}点，期望{}个点，步长间隔异常：\n触发时间：{}\n位置：{}'.format(symbol, days, len(
                        #         response["result"]["list"]), expect_num, datetime.datetime.now().strftime(
                        #         "%Y-%m-%d %H:%M:%S"), (last_time, next_time)))

                        break
                    else:
                        pass
            else:
                pass

    # 交易所列表
    def get_getExchanges(self, order=None, getExchangesList=None):
        url = self.url_file['Exchanges']['getExchanges']
        # 判断是否执行排序测试用例
        if not order:
            defaultData = self.ReadAndWrite.load_data(filePath=r'data\getExchangesList.yaml')[1]
            response = self.send.main_request(methods='GET', url=url, params=defaultData)
            # 自动写入用例驱动，写完关闭需要添加固定等待时间
            self.ReadAndWrite.clear_data(filePath=r'data\exchange.yaml', headline=True, needWriteData=[{
                "exchange_id": "exchange_id", "day": "day"}])
            dayList = [7, 30, 90, -1, 0]
            for exchange in response['result']['items']:
                for day in dayList:
                    if "exchange_id" in exchange:
                        data = [{
                            "exchange_id": exchange["exchange_id"],
                            "day": day
                        }]

                        self.ReadAndWrite.write_data(filePath=r"data\exchange.yaml", needWriteData=data)
                    else:
                        break
        if order:
            getExchanges = self.ReadAndWrite.load_data(filePath=r'data\getExchangesList.yaml')
            response = self.send.main_request(methods='GET', url=url, params=getExchanges)

    # 交易所信息
    def get_getExchangeInfo(self, exchange):
        url = self.url_file['Exchanges']['getExchangeInfo']
        self.send.main_request(methods="GET", url=url, params=exchange)

    # 交易所指数趋势
    def get_getExchangeChart(self, ExchangeChart):
        url = self.url_file['Exchanges']['getExchangeChart']
        self.send.main_request(methods="GET", url=url, params=ExchangeChart)

    # 交易所交易对
    def get_getExchangePairsList(self, getExchangePairsList):
        url = self.url_file['Exchanges']['getExchangeChart']
        self.send.main_request(methods="GET", url=url, params=getExchangePairsList)

# if __name__ == '__main__':
#     run = MarketsPage(env="releaseEnvironment", urlFile="data\\api.yaml", apiVersion="v1_2_1", app_version="1.4.1")
#     run.get_accessToken()
#     run.get_tools_list()
# run.getDiscoverCoinList()
# run.get_cexList(pageSize=20, one=True)
