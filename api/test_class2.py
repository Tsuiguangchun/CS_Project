# encoding:utf-8
# @CreateTime: 2022/8/2 17:02
# @Author: Xuguangchun
# @FlieName: test_class2.py
# @SoftWare: PyCharm

from api.test_class import *
from common.log import *
import jsonpath
from common.get_data import *
response = [{'code': 40001, 'message': 'client-check-error:Signature failed.',
             'result': {}, 'request_id': '97F39E7E-113A-74F7-D878-295E44B44CA2', 'response_time': 1659501786,
             'is_white_list': 1}]
"""

data = jsonpath.jsonpath(response, '$.request_id[1]')
print(data)
"""
"""
class TT2(TT):

    def assert_data(self):

        assert response['code'] == 0
        CSLog().log('接口请求状态：成功')
        try:
            assert len(response['result']) == 1
            print(response["result"], type(response["result"]), len(response["result"]))
            # print("请求成功，但是数据校验失败：result返回是一个空字典")
        except AssertionError as msg:
            CSLog().log("请求成功，但是数据校验失败：result返回是一个空字典", msg)
        #     else:
        #         pass
        #         # write_data(filePath="data\\result_IsEmpty.yaml", needWriteData=url)
        # else:
        #     CSLog().log('接口请求状态：失败')

    def get_coinId(self):
        print(self.coinId)


if __name__ == '__main__':
    T = TT(coinId="5555", symbol="oPopL")
    T2 = TT2(coinId="6666", symbol="oPopL")
    T2.myTest()
    T2.get_coinId()
    T2.myList()
    T2.assert_data()
"""

"""
def testPlay(order=None):
    if order is False:
        print("开始就结算")
    if order is True:
        print("开始吧")


testPlay(order=True)
"""

import os, time

# path = r"../data/token.yaml"
path = r'D:\cs_project\data\token.yaml'
# print(ReadAndWrite().load_data(path))
# print(len(ReadAndWrite().load_data(path)))
# print(ReadAndWrite().load_data(path)[0]['access-token'])
token = ReadAndWrite().load_data(path)

# print(os.path.exists(path))


# if os.path.exists(path) and "access-token" in token[0]:
#     print("True")
#     if int(time.time()) <= token[0]['expire_time']:
#         print("未过期")
#     else:
#
#         print('已过期')
# else:
#     print("False")
#
# def yes(num=None):
#     num = 1
#     b = num
#     print(2)
#
# yes()
# def runAll(num, one=False):
#     if not one:
#         a = num
#         print("False", a)
#     else:
#         a = 4 + num
#         print("True", a)
#
#
# runAll(6, one=False)

# li = [[1, 2, 2, 4, "aa", "bb", "aa", "dd", "cc", 1]]
# new_list = list(set(li[0]))
# new_list.sort(key=li[0].index)
# print(new_list)
# a = None
# new_a = set(a)
# print(new_a)

# def test():
#     ReadAndWrite().clear_data(filePath='data/test1.yaml')
#     num = 0
#     while num < 3:
#         num += 1
#         ReadAndWrite().write_data(filePath='data/test1.yaml', needWriteData=response)
# test()
# if int(time.time()) >= ReadAndWrite().load_data(path)['expire_time']:
# import datetime
#
# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
# data = {'day': 7}
# data.update({"day": 9, "data": (1648512000, 1654041600)})
# print(data)
ree = ReadAndWrite().load_data(filePath=r'data\coinsPrice_chart_duration.yaml')
print(json.dumps(ree, indent=4))
# print(1%19)
