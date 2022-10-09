# encoding:utf-8
# @CreateTime: 2022/7/11 16:31
# @Author: Xuguangchun
# @FlieName: assertScript.py
# @SoftWare: PyCharm

import pytest
from common.log import *
from common.get_data import *
from common.requestMethod import *
from common.sendMsg_DingTalk import *


def assertion(response, response_time, url, header, params):
    if response['code'] == 0:
        CSLog().log('接口请求状态：成功')
        if len(response['result']) == 0:
            CSLog().log("数据校验失败：result返回是一个空字典\n", response)
            empty_request_url = [{"address": url, "body": params}]
            ReadAndWrite().write_data(filePath="data\\result_IsEmpty.yaml", needWriteData=empty_request_url)
            assert len(response['result']) != 0
    else:
        CSLog().log('接口请求状态：失败')
        fail_request_url = [{"address": url, "body": params}]
        ReadAndWrite().write_data(filePath="data\\request_Fail.yaml", needWriteData=fail_request_url)
        DingTalk().errorLog_sending(logData="接口请求失败：\n\n 请求地址:{0}\n 请求头:{1}\n请求参数:{2}\n响应内容：{3}"
                                            .format(url, header, params, response))
        assert response['code'] == 0

    if response_time <= 3:
        pass
    else:
        CSLog().log("请求响应时间超过3秒，当前响应时间为：%f" % response_time)
        timeout_url = [{"url": url, "body": params}]
        ReadAndWrite().write_data(filePath="data\\responseTime_Over3s.yaml", needWriteData=timeout_url)
        DingTalk().errorLog_sending(logData="请求响应时间超过3秒，当前响应时间为：{0}\n\n 请求地址:{1}\n 请求头:{2}\n"
                                            "请求参数:{3}".format(response_time, url, header, params))
        assert response_time <= 3
