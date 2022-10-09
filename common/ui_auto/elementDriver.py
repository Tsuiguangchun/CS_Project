# encoding:utf-8
# @CreateTime: 2022/8/1 10:33
# @Author: Xuguangchun
# @FlieName: elementDriver.py
# @SoftWare: PyCharm

try:
    import uiautomator2 as u2
except ImportError as e:
    print("请先安装 pip install --pre uiautomator2", e)
import time
import re

"""
{
    "package": "com.coinsky.android",
    "activity": "com.ai.chain.activity.main.MainActivity"
}
"""

"""
# 等待页面加载
d.wait_activity()
#等待元素出现
d().wait()
#等待元素小时
d().wait_gone()
#等待元素是否存在
d().exit()
"""


class Base_page:
    def __init__(self, devices):
        self.driver = u2.connect(addr=devices)
        self.driver.implicitly_wait(5)
        self.message = self.driver.toast.get_message()

    def start_app(self, package_name, activity):
        try:
            self.driver.app_start(package_name=package_name, activity=activity)
            if self.driver.app_wait(package_name=package_name):
                print("{} App运行成功！".format(package_name))
            else:
                print("{} App运行失败！".format(package_name))
                self.driver.app_stop(package_name=package_name)
                self.driver.app_start(package_name=package_name, activity=activity)
        except Exception as msg:
            return '检查启动包名和activity是否错误', msg

    # 1、传入attribute元素定位属性(定位方式)判断，2、value元素定位值
    def element_click(self, attribute, value):
        # xpath绝对路径点击
        try:
            if attribute == "xpath":
                return self.driver.xpath(value).click(timeout=3)

            # 文本元素点击
            elif attribute == "text":
                return self.driver(text=value).click(timeout=3)

            # 元素组[索引]点击
            elif attribute == "className":
                return self.driver(className=value).click(timeout=3)

            # 控件元素id点击
            elif attribute == "resourceId":
                return self.driver(resourceId=value).click(timeout=3)

            # 通过元素描述内容点击
            elif attribute == "Description":
                return self.driver(Description=value).click(timeout=3)

        except Exception as msg:
            return "元素定位失败检查定位元素值是否正确！", msg

    # 1、attribute传入元素定位方式，2、elementValue 定位元素值，3、sendContent 发送内容关键词
    def send_keys(self, attribute, elementValue, sendContent):

        try:
            if attribute == "resourceId":
                self.driver(resourceId=elementValue).wait(3)
                return self.driver(resourceId=elementValue).send_keys(sendContent)

            elif attribute == "xpath":
                return self.driver.xpath(elementValue).set_text(sendContent)
        except Exception as msg:
            return "关键词发送失败", msg

    """
     # xpath绝对路径点击
    def xpath_click(self, xpath):
        self.driver.xpath(xpath).click(timeout=3)

    # 文本元素点击
    def text_click(self, textValue):
        self.driver(text=textValue).click(timeout=3)

    # 元素组[索引]点击
    def class_click(self, classValue):
        self.driver(className=classValue).click(timeout=3)

    # 控件元素id点击
    def resourceId_click(self, resourceIdValue):
        self.driver(resourceId=resourceIdValue).click(timeout=3)

    # 通过元素描述内容点击
    def Description_click(self, DescriptionValue):
        self.driver(Description=DescriptionValue).click(timeout=3)

    # 控件元素id定位输入框，输入关键字
    def resourceId_send(self, resourceIdValue, content):
        self.driver(resourceId=resourceIdValue).wait(3)
        self.driver(resourceId=resourceIdValue).send_keys(content)

    def xpath_send(self, resourceIdValue, content):
        self.driver.xpath(resourceIdValue).set_text(content)
    
    """

    # 坐标点击
    def zb_click(self, x, y):
        self.driver.click(x, y)

    # 滑动坐标
    def zb_swipe(self, x2, y2, x1, y1, *args):
        self.driver.swipe(x2, y2, x1, y1, *args)

    # 向左滑动
    def l_swipe(self):
        self.driver.swipe_ext("left", scale=0.9)

    # 向右滑动
    def r_swipe(self):
        self.driver.swipe_ext("right", scale=0.9)

    # 控件元素id定位输入框，清除输入关键字
    def content_clear(self, resourceIdValue, content):
        self.driver(resourceId=resourceIdValue).send_keys(content)

    # 截图文件保存路径
    def screenAndSave(self, imagePath):
        imageName = time.strftime("%Y%m%d%H%M%S")+".jpg"
        self.driver.screenshot(filename=imagePath + imageName)

    def recordAndSave(self, recordPath):
        self.driver.screenrecord(recordPath)
