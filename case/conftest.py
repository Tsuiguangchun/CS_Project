# encoding:utf-8
# @CreateTime: 2022/6/24 16:51
# @Author: Xuguangchun
# @FlieName: contest.py
# @SoftWare: PyCharm


import pytest
from common.requestMethod import *
from common.rsa_encode import *
from common.get_environment import *
from common.log import *
from common.get_data import *


@pytest.fixture(scope='session', autouse=False)
def get_accessToken(self):
    self.logger.log("=======token接口开始请求=======")
    url = self.url_file[0]["initApi"]["getToken"]
    data = ReadAndWrite().load_data("data\\bodyData.yaml")[0]['get_token']
    data.update({"app_key": self.app_key, "secret": rsa_encrypt(self.secret)})
    self.send.main_request(methods="POST", url=url, data=data)