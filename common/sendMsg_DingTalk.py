# encoding:utf-8
# @CreateTime: 2022/8/8 1:22
# @Author: Xuguangchun
# @FlieName: sendMsg_DingTalk.py
# @SoftWare: PyCharm

import os, json, time
# import jenkins
import requests
from common.get_data import *

# 钉钉推送方法：
# filepath读取report文件中"prometheusData.txt"，循环遍历获取需要的值。
# 使用钉钉机器人的接口，拼接后推送text
# retries_run 运行总数
# status_passed 通过数量
# status_failed 不通过数量
# status_broken 脚本参数出错
# job_name 构建项目名称
# job_url 构建项目的地址
# job_last_number 当前构建的数字
# report_url 构建后allure 测试报告的地址
# "isAtAll": True 全部，False推送指定

# jenkins_url = 'http://192.168.6.131:8080'
# job_name = "Debug_UserReport"
# job_url = jenkins_url + '/job/' + job_name + '/'
# server = jenkins.Jenkins(jenkins_url, username='xuguangchun', password='8041308')
# time.sleep(3)
# job_last_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
# report_url = job_url + str(job_last_number) + '/allure'

# python 3.8
import time
import hmac
import hashlib
import base64
import urllib.parse


class DingTalk:

    readFile = ReadAndWrite()

    def __init__(self):
        self.session = requests.session()
        self.run_times = 0
        self.rotBot_index = 0

    def run_robot(self, sending_data):
        self.run_times += 1
        rotBot_file = ReadAndWrite().load_data(filePath=r'data\rotbot_webHook.yaml')
        timestamp = str(round(time.time() * 1000))
        header = {'content-type': 'application/json'}
        secret = rotBot_file[self.rotBot_index]['secret']
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        webHook = rotBot_file[self.rotBot_index]['webhook'] + '&sign=' + sign + '&timestamp=' + timestamp
        print("========>webHook地址", webHook)
        if self.run_times % 18 == 0 and self.run_times != 0:
            self.rotBot_index += 1
            time.sleep(3)
            r = self.session.post(webHook, headers=header, data=json.dumps(sending_data)).text
            r.encoding = 'utf-8'
            # r.text

        elif self.rotBot_index > 5:
            time.sleep(8)
            self.rotBot_index = 0
            r = self.session.post(webHook, headers=header, data=json.dumps(sending_data)).text
            r.encoding = 'utf-8'
            # r.text

        else:
            r = self.session.post(webHook, headers=header, data=json.dumps(sending_data)).text
            r.encoding = 'utf-8'
            # r.text

    def report_Sending(self, filepath):
        new_fail_request_url = None
        new_resultEmpty_request_url = None
        new_timeout_request_url = None
        new_error_priceChart = None
        new_error_marketsChart = None
        error_priceChart_num = 0
        error_marketsChart_num = 0

        d = {}
        f = open(filepath, 'r')
        for lines in f:
            for c in lines:
                launch_name = lines.strip('\n').split(' ')[0]
                num = lines.strip('\n').split(' ')[1]
                d.update({launch_name: num})
        f.close()

        retries_run = d.get('launch_retries_run')
        status_passed = d.get('launch_status_passed')
        status_failed = d.get('launch_status_failed')
        status_broken = d.get('launch_status_broken')
        min_runtime = d.get('launch_time_min_duration')

        fail_request_url = self.readFile.load_data(filePath=r'data\request_Fail.yaml')
        resultEmpty_request_url = self.readFile.load_data(filePath=r'data\result_IsEmpty.yaml')
        timeout_request_url = self.readFile.load_data(filePath=r'data\responseTime_Over3s.yaml')
        error_priceChart = self.readFile.load_data(filePath='data\\priceChart_error.yaml')
        error_marketsChart = self.readFile.load_data(filePath='data\\marketChart_error.yaml')
        gasReport = self.readFile.load_data(filePath=r'data\gasReport.yaml')
        print(gasReport)

        # 利用集合去重
        if fail_request_url is not None:
            new_fail_request_url = list(set(fail_request_url))
            # new_fail_request_url.sort(key=fail_request_url[0].index)

        if resultEmpty_request_url is not None:
            new_resultEmpty_request_url = json.dumps(resultEmpty_request_url)
            # new_resultEmpty_request_url.sort(key=resultEmpty_request_url[0].index)

        if timeout_request_url is not None:
            new_timeout_request_url = json.dumps(timeout_request_url)
            # new_timeout_request_url.sort(key=timeout_request_url[0].index)

        if error_priceChart is not None:
            new_error_priceChart = list(set(error_priceChart))
            error_priceChart_num = len(new_error_priceChart)
            # print(new_error_priceChart)

        if error_marketsChart is not None:
            new_error_marketsChart = list(set(error_marketsChart))
            error_marketsChart_num = len(new_error_marketsChart)

        _data = {
            "msgtype": "text",
            "text": {
                "content": "coinSky项目测试:"
                           "\n\n测试概述:"
                           "\n运行总数: " + retries_run +
                           "\n通过数量: " + status_passed +
                           "\n失败数量: " + status_failed +
                           "\n执行错误数量:" + status_broken +
                           "\n最快响应时间：" + min_runtime + "ms" +
                           "\n价格趋势图数据异常货币{0}个：{1}".format(error_priceChart_num, new_error_priceChart) +
                           "\n市值趋势图数据异常货币{0}个：{1}".format(error_marketsChart_num, new_error_marketsChart) +
                           "\nresult空数据url: " + str(new_resultEmpty_request_url) +
                           "\n请求响应时间超过3秒url：" + str(new_timeout_request_url) +
                           "\n请求失败url：" + str(new_fail_request_url) +
                           "\nEtherScan-Gwei校验结果：" + str(gasReport) +
                           "\n "
            },
            "at": {
                "atMobiles": [
                    "13682630240"
                ],
                "isAtAll": True
            }
        }
        self.run_robot(sending_data=_data)

    def errorLog_sending(self, *args, logData):

        data = {
            "msgtype": "text",
            "text": {
                "content": logData + '\n'
            },
            "at": {
                "atMobiles": [
                    "13682630240"
                ],
                "isAtAll": True
            }
        }
        self.run_robot(sending_data=data)


# if __name__ == '__main__':
#     DingTalk().report_Sending(r'D:\cs_project\report\allureReport\export\prometheusData.txt')
