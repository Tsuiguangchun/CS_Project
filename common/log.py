# encoding:utf-8
# @CreateTime: 2022/6/16 0:32
# @Author: Xuguangchun
# @FlieName: log.py
# @SoftWare: PyCharm

import logging
import json
"""
- %(pathname)s 
"""


class CSLog:
    fmt = "%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s"

    def __init__(self):
        pass

    def log(self, msg, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG, format=CSLog.fmt)

        return logging.info(msg)

    def consoleLogger_info(self, url, headers, params, response, response_time):
        logUrl = self.log("接口请求URL:%s" % url)
        logHeader = self.log("接口请求头：:%s" % headers)
        logParams = self.log("接口请求参数%s" % params)
        logResponse = self.log("接口响应内容:%s" % json.dumps(response, indent=4))
        logResponseTime = self.log("接口响应时间：%f秒" % response_time)

        return logUrl, logHeader, logParams, logResponse, logResponseTime
#
# if __name__ == '__main__':
#     log = CSLog()
#     name = 4
#     log.log("这是%d")