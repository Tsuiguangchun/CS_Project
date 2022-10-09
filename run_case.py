# encoding:utf-8
# @CreateTime: 2022/7/27 10:46
# @Author: Xuguangchun
# @FlieName: run_case.py
# @SoftWare: PyCharm

import pytest, time, sys, os

from case.test_allTestCase import *
from api.get_homePage import *
from api.get_marketPage import *
from common.sendMsg_DingTalk import *

sys.path.append(r'D:\cs_project\venv\Lib\site-packages')
# 获取 路径
# file_path = os.path.dirname(os.path.abspath(__file__))
# # 修改运行路径
# sys.path.append(file_path)
# # 0 表示优先级，数字越大级别越低，修改模块的导入
# sys.path.insert(0, os.path.dirname(file_path))
# Test_all_Case.homePage = HomePage(env="releaseEnvironment", urlFile="data\\api.yaml", apiVersion="v1_2_0")
Test_all_Case.cs = MarketsPage(env="releaseEnvironment", urlFile="data\\api.yaml", apiVersion="v1_2_1",
                               app_version="1.4.1")

# print(Test_all_Case.cs)

if __name__ == '__main__':
    """
    # 命令运行用例临时结果临时json数据 ：pytest -vs case/test_allTestCase.py --alluredir report/allureResult --clean-alluredir
    # 主函数执行allure与命令模式不同 ，每个参数要逗号分开，否则无法执行
    # 集成运行用例的临时json文件，生成测试报告
    """
    # pytest.main(['-vs', 'case/test_allTestCase.py'])
    pytest.main(['-vs', '-reruns=3', 'case/test_allTestCase.py', '--alluredir=./report/allureResult', '--clean-alluredir'])
    os.system('allure generate report/allureResult -o report/allureReport --clean')
    time.sleep(30)
    DingTalk().report_Sending(r'D:\cs_project\report\allureReport\export\prometheusData.txt')
