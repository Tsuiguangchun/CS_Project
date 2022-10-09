# encoding:utf-8
# @CreateTime: 2022/6/20 23:09
# @Author: Xuguangchun
# @FlieName: get_environment.py
# @SoftWare: PyCharm

from common.get_data import *

"""
# 这写死配置文件路径，因为懒，可以放到init函数下动态传入
"""


class ApiInit:
    initApiData = ReadAndWrite().load_data(filePath="data\initApiData.yaml")

    def __init__(self, env):
        self.host = ApiInit.initApiData[env]['host']
        self.appKey = ApiInit.initApiData[env]["appkey"]
        self.secret = ApiInit.initApiData[env]["secret"]
        self.ase_key = ApiInit.initApiData[env]["ase_key"]
        self.ase_iv = ApiInit.initApiData[env]["ase_iv"]

    def get_env(self):

        # print("打印====", self.host, self.appKey, self.secret, self.ase_key, self.ase_iv)
        return self.host, self.appKey, self.secret, self.ase_key, self.ase_iv

#
# if __name__ == '__main__':
#     a = ApiInit(env="testEnvironment")
#     a.get_env()
