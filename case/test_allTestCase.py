# encoding:utf-8
# @CreateTime: 2022/7/29 17:37
# @Author: Xuguangchun
# @FlieName: test_allTestCase.py
# @SoftWare: PyCharm


from api.get_homePage import *
from api.get_marketPage import *
from common.log import *
import pytest
import allure


@allure.epic("CoinSky 项目")
@allure.feature("主功能")
class Test_all_Case:
    # cs类变量,调用APi模块业务初始化接口实例化的对象，注意类的继承关系
    cs = None
    logger = CSLog()

    # ReadAndWrite() = ReadAndWrite()()

    @pytest.fixture(scope="class", autouse=True)
    def get_token(self):
        self.logger.log("=======token接口开始请求=======")
        self.cs.get_accessToken()

    @pytest.mark.dependency(name='test_cexList')
    def test_cexList(self):
        allure.dynamic.story("行情模块")
        allure.dynamic.title("获取Cex行情列表前50")
        with allure.step("获取cex市值排名前50货币的coin_id 和交易所信息"):
            self.logger.log("=========Cex列表接口开始请求=========")
            self.cs.get_cexList(pageSize=50, one=False)
            # print("========================", data)

    time.sleep(5)

    @pytest.mark.parametrize('cexCoinInfo', ReadAndWrite().load_data(filePath=r'data\\getCexInfo.yaml'))
    # @pytest.mark.dependency(depends=['test_cexList'], scope='package')
    def test_cexCoinInfo(self, cexCoinInfo):
        allure.dynamic.story("行情模块")
        allure.dynamic.title("访问{}:详情接口".format(cexCoinInfo['symbol']))
        with allure.step('从cex列表页拿到{}货币参数'.format(cexCoinInfo['symbol'])):
            self.logger.log("=========cex-->{}货币详情页接口开始请求=========".format(cexCoinInfo['symbol']))
            self.cs.get_cexCoinInfo(cexCoinInfo=cexCoinInfo)

    @allure.step('交易所信息请求参数：{}')
    @pytest.mark.parametrize('exchange', ReadAndWrite().load_data(filePath=r'data\exchange.yaml'))
    def test_ExchangeInfo(self, exchange):
        allure.dynamic.story("交易所模块")
        allure.dynamic.title("检查{}交易所信息：".format(exchange["exchange_id"]))
        self.logger.log("======={}交易所信息开始请求".format(exchange["exchange_id"]))
        self.cs.get_getExchangeInfo(exchange=exchange)

    def test_getToolsList(self):
        allure.dynamic.story("首页")
        allure.dynamic.title("获取工具接口")
        self.logger.log("=======工具接口开始请求=======")
        response = self.cs.get_tools_list()

    @allure.title("获取’我的模块‘里的推荐入口")
    def test_UserRecommendToolbar(self):
        allure.dynamic.story("个人中心页动态栏")
        allure.dynamic.title("获取’我的模块‘里的推荐入口")
        self.logger.log("=========我的模块入口开始请求=========")
        response = self.cs.get_UserRecommendToolbar()

    @allure.title("获取热门搜索合约榜单")
    def test_HotSearchContract(self):
        self.logger.log("=======热门搜索合约接口开始请求=======")
        response = self.cs.get_HotSearchContract()
        allure.dynamic.title("获取热门搜索合约榜单")

    def getDiscoverCoinList(self):
        allure.dynamic.story("首页")
        allure.dynamic.title("获取发现页列表")
        self.logger.log("=======发现页接口开始请求=======")
        response = self.cs.getDiscoverCoinList()

    @pytest.mark.parametrize('cexCoinInfo', ReadAndWrite().load_data(filePath='data\\getCexInfo.yaml'))
    def test_cexCoinChart(self, cexCoinInfo):
        allure.dynamic.story("行情模块")
        allure.dynamic.title("访问{}:价格趋势图数据".format(cexCoinInfo['symbol']))
        self.logger.log("=========cex-->{}货币详情页价格趋势图数据开始请求=========".format(cexCoinInfo['symbol']))
        self.cs.get_cexCoinChart(cexCoinInfo=cexCoinInfo)

    @pytest.mark.parametrize('cexCoinInfo', ReadAndWrite().load_data(filePath='data\\getCexInfo.yaml'))
    def test_MarketCapChart(self, cexCoinInfo):
        allure.dynamic.story("行情模块")
        allure.dynamic.title("访问{}:市值趋势图数据".format(cexCoinInfo['symbol']))
        self.logger.log("=========cex-->{}货币详情页市值趋势图数据开始请求=========".format(cexCoinInfo['symbol']))
        self.cs.get_MarketCapChart(cexCoinInfo=cexCoinInfo)

    @allure.step('交易所列表请求参数：{}')
    # 由于parametrize这里传参默认文件内用例都会被执行，无法执行默认值
    # @pytest.mark.parametrize('getExchangesList', ReadAndWrite().load_data(filePath='data\\getExchangesList.yaml'))
    def test_Exchanges(self, getExchangesList=None):
        allure.dynamic.story("交易所模块")
        allure.dynamic.title("检查交易所列表以{}排序方式访问：".format(getExchangesList))
        self.logger.log("=========交易所接口开始请求=========")
        self.cs.get_getExchanges(order=False)
        # time.sleep(3)

    @allure.step('交易所交易额趋势图请求参数：{}')
    @pytest.mark.parametrize('exchangeChart', ReadAndWrite().load_data(filePath=r'data\exchange.yaml'))
    def test_ExchangeChart(self, exchangeChart):
        allure.dynamic.story("交易所模块")
        allure.dynamic.title("检查{}交易所交易额{}天的趋势图信息：".format(exchangeChart["exchange_id"], exchangeChart["day"]))
        self.logger.log("======={}交易所指数趋势开始请求".format(exchangeChart["exchange_id"]))
        self.cs.get_getExchangeChart(ExchangeChart=exchangeChart)

    @allure.step('交易所列表请求参数：{}')
    @pytest.mark.parametrize('getExchangePairsList', ReadAndWrite().load_data(filePath=r'data\exchange.yaml'))
    def test_ExchangePairsList(self, getExchangePairsList):
        allure.dynamic.story("交易所模块")
        allure.dynamic.title("检查{}交易所交易对信息：".format(getExchangePairsList["exchange_id"]))
        self.logger.log("======={}交易所交易对开始请求".format(getExchangePairsList["exchange_id"]))
        self.cs.get_getExchangePairsList(getExchangePairsList=getExchangePairsList)

    def test_get_chainSetting(self):
        allure.dynamic.story("工具")
        allure.dynamic.title("gas配置")
        self.cs.get_chainSetting()

    def test_get_gas(self):
        allure.dynamic.story("工具")
        allure.dynamic.title("gas追踪")
        self.logger.log('=========gas追踪接口开始请求：=========')
        self.cs.get_gas()

    def test_get_nft_track(self):
        allure.dynamic.story("工具")
        allure.dynamic.title("nft mints tracker 列表")
        self.logger.log('=========nft mints tracker 列表接口开始请求：=========')
        self.cs.get_nft_track()

    time.sleep(3)

    if ReadAndWrite().load_data(filePath=r'data\nftTracker_Info.yaml') is not None:
        @pytest.mark.parametrize('nftTracker_Info', ReadAndWrite().load_data(filePath=r'data\nftTracker_Info.yaml'))
        def test_get_nft_info(self, nftTracker_Info):
            allure.dynamic.story("工具")
            allure.dynamic.title("nft mints- {}详情".format(nftTracker_Info['address']))
            self.logger.log('=========nft mints tracker 列表接口开始请求：=========')
            self.cs.get_nft_info(nftTracker_Info=nftTracker_Info)


Test_all_Case.cs = MarketsPage(env="releaseEnvironment", urlFile="data\\api.yaml", apiVersion="v1_2_1",
                               app_version="1.4.1")

if __name__ == '__main__':
    pytest.main(['-vs', "test_allTestCase.py", '-reruns=3'])
#     pytest.main(['-vs', "test_allTestCase.py", "--alluredir = report/allureResult", "--clean-alluredir"])
# pytest.main(['-vs', 'test_allTestCase.py', '--alluredir report/allureResult --clean-alluredir'])
# os.system('allure generate report/allureResult -o report/allureReport --clean')
