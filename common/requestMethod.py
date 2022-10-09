# encoding:utf-8
# @CreateTime: 2022/7/6 15:34
# @Author: Xuguangchun
# @FlieName: requestMethod.py
# @SoftWare: PyCharm

import requests
import json, time, re

from common.resultDecode import *
from common.get_environment import *
from common.baseHeader import *
from common.log import *
from common.assertScript import *
from common.get_data import *
from common.sendMsg_DingTalk import *

"""
1、初始化当前环境的相关信息（host、api相关密钥、头部信息等）
2、结合业务请求思路：
    》api版本控制,通过re.sub正则表达式进行替换版本号
    》传入访问url，请求体、请求头部信息
    》将加密数据进行解密
    》将解密内容更新到当前响应内容
    》数据解析，判断响应内容是否有访问令牌信息，令牌将访问token令牌放到请求头部
    》请求响应时长，数据校验
    》异常实时通知

"""


class Send_api:
    # logInfo = None

    def __init__(self, env, apiVersion, app_version):
        self.envInfo = ApiInit(env)
        self.host = self.envInfo.get_env()[0]
        self.app_key = self.envInfo.get_env()[1]
        self.secret = self.envInfo.get_env()[2]
        self.headers = RequestHeader(env=env, app_version=app_version)
        self.result_aes = AesSample(env)
        self.baseHeaders = self.headers.headers
        self.logger = CSLog()
        self.apiVersion = apiVersion
        self.dingTalk = DingTalk()
        self.session = requests.session()

    def consoleLogger_info(self, url, headers, params, response, response_time):
        logUrl = self.logger.log("接口请求URL: %s" % url)
        logHeader = self.logger.log("接口请求头：%s" % headers)
        logParams = self.logger.log("接口请求参数: %s" % params)
        logResponse = self.logger.log("接口响应内容: %s" % json.dumps(response))
        logResponseTime = self.logger.log("接口响应时间：%f秒" % response_time)
        return logUrl, logHeader, logParams, logResponse, logResponseTime

    def main_get(self, url, params=None, retry_times=1, **kwargs):
        response = None
        currentRetry_times = 0
        while currentRetry_times < retry_times:

            try:
                url = self.host + re.sub(pattern='[$].apiVersion.', repl=self.apiVersion, string=url)
                # print("当前版本url:", url)
                headers = self.headers.get_headers(url)
                r = self.session.get(url=url, params=params, headers=headers, verify=False, timeout=15, **kwargs)
                response_time = r.elapsed.total_seconds()
                response = r.json()  # json字符串格式化返回一个字典类型
                result = response['result']

                result_decode = self.result_aes.decode(result)
                response.update({"result": result_decode})
                assertion(response=response, response_time=response_time, url=url, header=headers, params=params)
                self.consoleLogger_info(url=url, headers=headers, params=params, response=response,
                                        response_time=response_time)
                if r.status_code == 200 and response['code'] == 0:
                    break
            except requests.exceptions.ConnectionError as e:
                currentRetry_times += 1
                self.logger.log("ConnectionError! please wait 3 seconds errorMsg:{}".format(e))
                time.sleep(3)

            # except requests.exceptions.ChunkedEncodingError as e:
            #     currentRetry_times += 1
            #     self.logger.log("ChunkedEncodingError! please wait 3 seconds errorMsg:{}".format(e))
            #     time.sleep(3)
            except:
                currentRetry_times += 1
                self.logger.log("UnknownError! please wait 3 seconds try request")
                time.sleep(1)
        return response

    def main_post(self, url, data=None, json=None, retry_times=1, **kwargs):  # headers=None
        response = None
        currentRetry_times = 0
        while currentRetry_times < retry_times:
            try:
                url = self.host + re.sub(pattern='[$].apiVersion.', repl=self.apiVersion, string=url)
                headers = self.headers.get_headers(url)
                r = self.session.post(url=url, data=data, json=json, headers=headers, timeout=15, **kwargs)
                response_time = r.elapsed.total_seconds()
                response = r.json()
                result = response['result']

                result_decode = self.result_aes.decode(result)
                response.update({"result": result_decode})
                assertion(response=response, response_time=response_time, url=url, header=headers, params=data)
                self.consoleLogger_info(url=url, headers=headers, params=data, response=response,
                                        response_time=response_time)

                if 'access_token' in result_decode:
                    access_token = result_decode['access_token']
                    expire_time = int(time.time()) + result_decode['expire_in'] - 1800  # 提前30分钟更新
                    token_info = {
                        "access-token": access_token,
                        "expire_time": expire_time
                    }
                    self.baseHeaders.update({"access-token": access_token})  # 将access-token 传入请求头
                    ReadAndWrite().write_data(filePath=r"data/token.yaml", needWriteData=token_info)
                    self.logger.log("传入token请求头:%s" % headers)
                else:
                    pass
                if r.status_code == 200:
                    break
                #     return response
                # return response
            except requests.exceptions.ConnectionError as e:
                currentRetry_times += 1
                self.logger.log("ConnectionError! please wait 7 seconds errorMsg:{}".format(e))
                time.sleep(2)
            except:
                currentRetry_times += 1
                self.logger.log("UnknownError! please wait 3 seconds")
                time.sleep(3)
        return response

    def main_request(self, methods, url, params=None, data=None, json=None, **kwargs):
        if methods == "GET":
            return self.main_get(url=url, params=params, **kwargs)
        if methods == "POST":
            return self.main_post(url=url, data=data, json=json, **kwargs)

        else:
            return "others request methods is not write,please check 'requestMethods.py' "


"""
class RequestHandler:
    def __init__(self):
        # session管理
        self.session = requests.session()
    def visit(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        return self.session.request(method,url, params=params, data=data, json=json, headers=headers,**kwargs)
    def close_session(self):
        # 关闭session
        self.session.close()
"""
#

#
# if __name__ == '__main__':
#    Send_api(env="releaseEnvironment")
