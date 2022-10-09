# encoding:utf-8
# @CreateTime: 2022/3/15 15:33
# @Author: Xuguangchun
# @FlieName: baseHeader.py
# @SoftWare: PyCharm

import hashlib, sys
import hmac
import random
import uuid
import string
import time
import json
from common.get_environment import *
from fake_useragent import UserAgent
# from common.log import *
sys.path.append(r"D:\cs_project\venv\Lib\site-packages")

# :类属性
# :headers 放公共基础请求头
# :self.url 构造函数内传入，每次调用类方法时需要传入url
# :self.key 这个是sign加密密钥，每次调用类方法时需要传入key
# ::类方法
# ：：get_noneStr 生成八位随机数传入请求头
# ：：get_url url 进行md5加密传入公共请求头
# ：：getSignData &：：get_sign 签名请求头参数拼接和加密生成sign值传入公共请求头
# ：：get_headers 调用类方法中传入公共请求头


class RequestHeader(object):

    def __init__(self, env=None, app_version=None):
        self.envInfo = ApiInit(env)
        self.key = self.envInfo.get_env()[2].encode('utf-8')
        self.app_key = self.envInfo.get_env()[1]
        self.app_version = app_version
        self.user_agent = UserAgent().random
        self.headers = {
            'app-version': self.app_version,
            'app-key': self.app_key,
            'client': 'Android',
            'uuid': str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name='coinSky')),
            'lang': 'EN',
            'access-token': '',
            'timezone': '0',
            'device-info': '{id = python38,device = testdevices2,brand = google,hardware = sailfish,product = sailfish,manufacturer = Google,model = opppo}',
            'User-Agent': self.user_agent,
            'Connection': 'keep-alive',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    # Mozilla / 5.0(Windows
    # NT
    # 5.1) AppleWebKit / 537.36(KHTML, like
    # Gecko) Chrome / 41.0
    # .2224
    # .3
    # Safari / 537.36
    def get_noneStr(self):
        # headers = self.headers
        seed = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        pingStr = []
        for i in range(8):
            pingStr.append(random.choice(seed))
        noneStr = ''.join(pingStr).upper()
        timestamp = str(int(time.time()))
        self.headers.update({"nonce": noneStr, "timestamp": timestamp})
        return noneStr

    def get_url(self, url):
        urlStr = url.lower()
        md5_urlStr = hashlib.md5(urlStr.encode('utf-8')).hexdigest()
        self.headers.update({"api_url": md5_urlStr})
        # update({"api_url": md5_urlStr})
        return md5_urlStr

    def getSignData(self):
        pingSign = []
        signData = ''
        notJoinPara = ["app-version", "app-key", "timestamp", "nonce", "client", "uuid", "lang", "access-token",
                       "api_url"]
        for key in sorted(self.headers.keys()):
            for k in notJoinPara:
                if key == k:
                    pingSign.append(key + "=" + self.headers[key])

        for i in pingSign:
            signData += i + "&"
        signData = signData[:-1]  # 剔除末尾&
        # print("这个是拼接结果：", signData)
        return signData

    def get_sign(self):
        hmac_signCode = hmac.new(self.key, bytes(self.getSignData(), encoding='utf-8'),
                                 hashlib.sha256).hexdigest().upper()
        self.headers.update({"signature": hmac_signCode})
        return hmac_signCode
        # return self.headers

    def get_headers(self, url):
        self.get_noneStr()
        self.get_url(url=url)
        self.get_sign()

        # print("我是请求头：", json.dumps(self.headers, indent=4))
        return self.headers

#
# if __name__ == '__main__':
#     test = RequestHeader(env="testEnvironment", url="/tet")
#
#     test.get_headers()
#     test.getSignData()
