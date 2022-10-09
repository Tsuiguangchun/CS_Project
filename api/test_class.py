# encoding:utf-8
# @CreateTime: 2022/8/2 17:00
# @Author: Xuguangchun
# @FlieName: test_class.py
# @SoftWare: PyCharm
import re

import jsonpath

class TT:
    def __init__(self, coinId, symbol):
        self.coinId = coinId
        self.symbol = symbol

    def myTest(self):
        print(self.coinId)

    def myList(self):
        dayList = [7, 30, 90, -1, 0]
        for i in dayList:
            print(i)

    def myData2(self):
        data = {
    "code": 0,
    "message": "Request succeeded.",
    "result": {
        "paging": {
            "page_no": 1,
            "page_size": 50,
            "total": 395
        },
        "items": [
            {
                "time": "0",
                "coin_id": "bitcoin",
                "icon": "https://coinsky.s3.us-west-1.amazonaws.com/coin-icon/20220211/bitcoin.png",
                "exchange": "binance",
                "symbol": "BTC",
                "fullname": "Bitcoin",
                "currency": "USDT",
                "price": "23164.76",
                "market_cap": 442572069246.72,
                "rank": 1,
                "volume_24h": 26183097878.29343,
                "rate_list": {
                    "1day_rate": 1.82,
                    "7day_rate": -0.10379997610920148,
                    "30day_rate": 14.588025439646135,
                    "90day_rate": -36.3114532796436,
                    "ytd_rate": -51.459610897550746,
                    "365day_rate": 0,
                    "allday_rate": 440.5910741456403,
                    "1day_price": 22750.97,
                    "7day_price": 23188.83,
                    "30day_price": 20215.69,
                    "90day_price": 36371.94,
                    "ytd_price": 47722.65,
                    "365day_price": 0,
                    "allday_price": 4285.08
                },
                "data_source": "cex",
                "channel_info": "cex_info_bitcoin_btc"
            },
            {
                "time": "0",
                "coin_id": "ethereum",
                "icon": "https://coinsky.s3.us-west-1.amazonaws.com/coin-icon/20220211/ethereum.png",
                "exchange": "binance",
                "symbol": "ETH",
                "fullname": "Ethereum",
                "currency": "USDT",
                "price": "1657.54",
                "market_cap": 201550833787.6355,
                "rank": 2,
                "volume_24h": 16574995227.089603,
                "rate_list": {
                    "1day_rate": 3.17,
                    "7day_rate": 0.20736226732200785,
                    "30day_rate": 43.10603836789667,
                    "90day_rate": -39.288696798769315,
                    "ytd_rate": -55.981346632886655,
                    "365day_rate": 0,
                    "allday_rate": 448.85430463576154,
                    "1day_price": 1606.61,
                    "7day_price": 1654.11,
                    "30day_price": 1158.26,
                    "90day_price": 2730.2,
                    "ytd_price": 3765.54,
                    "365day_price": 0,
                    "allday_price": 302
                },
                "data_source": "cex",
                "channel_info": "cex_info_ethereum_eth"
            },
            {
                "time": "0",
                "coin_id": "tether",
                "icon": "https://coinsky.s3.us-west-1.amazonaws.com/coin-icon/20220211/tether.png",
                "exchange": "binance",
                "symbol": "USDT",
                "fullname": "Tether",
                "currency": "USDT",
                "price": "0.99981",
                "market_cap": 66414468698.31743,
                "rank": 3,
                "volume_24h": 46960403091.65048,
                "rate_list": {
                    "1day_rate": -0.02,
                    "7day_rate": -0.01900000000000235,
                    "30day_rate": 0.03101550775386908,
                    "90day_rate": -0.04898530440867645,
                    "ytd_rate": -0.02899710028997225,
                    "365day_rate": 0,
                    "allday_rate": -0.01900000000000235,
                    "1day_price": 0.99999,
                    "7day_price": 1,
                    "30day_price": 0.9995,
                    "90day_price": 1.0003,
                    "ytd_price": 1.0001,
                    "365day_price": 0,
                    "allday_price": 1
                },
                "data_source": "cex",
                "channel_info": "cex_info_tether_usdt"
            },
            {
                "time": "0",
                "coin_id": "usd-coin",
                "icon": "https://coinsky.s3.us-west-1.amazonaws.com/coin-icon/20220211/usd-coin.png",
                "exchange": "binance",
                "symbol": "USDC",
                "fullname": "USD Coin",
                "currency": "USDT",
                "price": "0.9998",
                "market_cap": 54326686531.36462,
                "rank": 4,
                "volume_24h": 7069162726.263447,
                "rate_list": {
                    "1day_rate": -0.01,
                    "7day_rate": 0.010003000900268979,
                    "30day_rate": -0.12985715712716797,
                    "90day_rate": -0.03999200159967566,
                    "ytd_rate": 0,
                    "365day_rate": 0,
                    "allday_rate": -1.1469250543800724,
                    "1day_price": 0.9999,
                    "7day_price": 0.9997,
                    "30day_price": 1.0011,
                    "90day_price": 1.0002,
                    "ytd_price": 0.9998,
                    "365day_price": 0,
                    "allday_price": 1.0114
                },
                "data_source": "cex",
                "channel_info": "cex_info_usd-coin_usdc"
            },
            {
                "time": "0",
                "coin_id": "bnb",
                "icon": "https://coinsky.s3.us-west-1.amazonaws.com/coin-icon/20220211/bnb.png",
                "exchange": "binance",
                "symbol": "BNB",
                "fullname": "BNB",
                "currency": "USDT",
                "price": "301",
                "market_cap": 48514114409.763,
                "rank": 5,
                "volume_24h": 2160648877.8484135,
                "rate_list": {
                    "1day_rate": 7.19,
                    "7day_rate": 11.316568047337288,
                    "30day_rate": 28.68747327917913,
                    "90day_rate": -20.222634508348797,
                    "ytd_rate": -42.91674568556798,
                    "365day_rate": 0,
                    "allday_rate": 19059.770846594525,
                    "1day_price": 280.8,
                    "7day_price": 270.4,
                    "30day_price": 233.9,
                    "90day_price": 377.3,
                    "ytd_price": 527.3,
                    "365day_price": 0,
                    "allday_price": 1.571
                },
                "data_source": "cex",
                "channel_info": "cex_info_bnb_bnb"
            },
            {
                "time": "0",
                "coin_id": "xrp",
                "icon": "https://coinsky.s3.us-west-1.amazonaws.com/coin-icon/20220211/xrp.png",
                "exchange": "binance",
                "symbol": "XRP",
                "fullname": "XRP",
                "currency": "USDT",
                "price": "0.3729",
                "market_cap": 18012639506.0022,
                "rank": 6,
                "volume_24h": 1074832771.851827,
                "rate_list": {
                    "1day_rate": 2.39,
                    "7day_rate": 3.439667128987524,
                    "30day_rate": 14.281336193686803,
                    "90day_rate": -37.97405189620758,
                    "ytd_rate": -56.165510755848125,
                    "365day_rate": 0,
                    "allday_rate": -58.0964153275649,
                    "1day_price": 0.3642,
                    "7day_price": 0.3605,
                    "30day_price": 0.3263,
                    "90day_price": 0.6012,
                    "ytd_price": 0.8507,
                    "365day_price": 0,
                    "allday_price": 0.8899
                },
                "data_source": "cex",
                "channel_info": "cex_info_xrp_xrp"
            },
            {
                "time": "0",
                "coin_id": "binance-usd",
                "icon": "https://coinsky.s3.us-west-1.amazonaws.com/coin-icon/20220211/binance-usd.png",
                "exchange": "binance",
                "symbol": "BUSD",
                "fullname": "Binance USD",
                "currency": "USDT",
                "price": "0.9998",
                "market_cap": 17919949983.60115,
                "rank": 7,
                "volume_24h": 5404544355.308909,
                "rate_list": {
                    "1day_rate": 0,
                    "7day_rate": 0.010003000900268979,
                    "30day_rate": -0.12985715712716797,
                    "90day_rate": -0.03999200159967566,
                    "ytd_rate": 0,
                    "365day_rate": 0,
                    "allday_rate": -0.019999999999997797,
                    "1day_price": 0.9998,
                    "7day_price": 0.9997,
                    "30day_price": 1.0011,
                    "90day_price": 1.0002,
                    "ytd_price": 0.9998,
                    "365day_price": 0,
                    "allday_price": 1
                },
                "data_source": "cex",
                "channel_info": "cex_info_binance-usd_busd"
            },
            {
                "time": "0",
                "coin_id": "cardano",
                "icon": "https://coinsky.s3.us-west-1.amazonaws.com/coin-icon/20220211/cardano.png",
                "exchange": "binance",
                "symbol": "ADA",
                "fullname": "Cardano",
                "currency": "USDT",
                "price": "0.5099",
                "market_cap": 17196931903.82123,
                "rank": 8,
                "volume_24h": 522588499.1314394,
                "rate_list": {
                    "1day_rate": 3.07,
                    "7day_rate": -0.4879000780640021,
                    "30day_rate": 9.467582653499363,
                    "90day_rate": -35.5046799898811,
                    "ytd_rate": -63.05072463768116,
                    "365day_rate": 0,
                    "allday_rate": 110.1813685078318,
                    "1day_price": 0.4947,
                    "7day_price": 0.5124,
                    "30day_price": 0.4658,
                    "90day_price": 0.7906,
                    "ytd_price": 1.38,
                    "365day_price": 0,
                    "allday_price": 0.2426
                },
                "data_source": "cex",
                "channel_info": "cex_info_cardano_ada"
            }]}}
        data1 = jsonpath.jsonpath(data, "$.result.items[0]")

        data2 = jsonpath.jsonpath(data, "$.result.items[*]['rate_list']")
        # for i in jsonpath.jsonpath(data1, "$.result.items[0].[?(@.365day_price <= 0)].symbol")
        data3 = data["result"]["items"][0]['price']
        data4 = {'1day_rate': 1.82, '7day_rate': -0.10379997610920148, '30day_rate': 14.588025439646135, '90day_rate': -36.3114532796436, 'ytd_rate': -51.459610897550746, '365day_rate': 0, 'allday_rate': 440.5910741456403, '1day_price': 22750.97, '7day_price': 23188.83, '30day_price': 20215.69, '90day_price': 36371.94, 'ytd_price': 47722.65, '365day_price': 0, 'allday_price': 4285.08}
        print("索引", data3,type(data3))
        print("data1:", data1)
        print("data2:", data2)
        print(data4['1day_rate'])
        # data5 = data3['1day_rate']
        data6 = jsonpath.jsonpath(data, "$...items[0][?(@.price='0.5099')]")
        # print(data5)
        print("data6",data6)
        data7 = '0.9999'
        print(float(data7))


        url = '/${Apiversion}/getToolsList.json'
        # data8 = re.search('^/Apiversion', url)
        # print(data8)
        # print(data8.group())
        data9 = re.sub('[$].Apiversion.',"1_2_0",url)
        print(data9)

if __name__ == '__main__':
    do = TT(1223, "nih")
    do.myData2()