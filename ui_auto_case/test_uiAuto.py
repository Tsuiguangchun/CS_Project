# encoding:utf-8
# @CreateTime: 2022/7/27 17:23
# @Author: Xuguangchun
# @FlieName: test_uiAuto.py
# @SoftWare: PyCharm


import uiautomator2 as u2
import time
import re
from common.ui_auto.elementDriver import *


if __name__ == '__main__':
    goUi = Base_page(devices='127.0.0.1:5555')
    goUi.start_app(package_name="com.coinsky.android", activity="com.ai.chain.activity.main.MainActivity")
    goUi.element_click(attribute="xpath", value='//*[@resource-id="com.coinsky.android:id/list_tool"]/android.widget.FrameLayout[4]')
    search = "com.coinsky.android:id/edit_search"
    search_btn = 'com.coinsky.android:id/btn_search'

    time.sleep(3)
    for i in range(len(goUi.driver(className='android.widget.TextView'))):
        d = goUi.driver(className='android.widget.TextView')[i].get_text(3)
        print(d)

    goUi.driver.press('back')
    time.sleep(3)
    goUi.element_click(attribute="resourceId", value=search_btn)
    goUi.send_keys(attribute="resourceId", elementValue=search, sendContent='noda')
    time.sleep(2.5)
    xml = goUi.driver.dump_hierarchy()
    print("页面的元素：", xml)
    if re.search(".*?BTC",xml):
        print("查询成功")
    else:
        print("查询失败")

    goUi.screenAndSave(imagePath=r'..\log\imageFile\\')

