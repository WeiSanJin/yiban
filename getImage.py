# -*- coding: utf-8 -*-
# @Time :2020/8/7 13:42
# @File : getImage.py
# @Author : weisanjin
# @Software: PyCharm
from selenium import webdriver
from yiban.config import url
import time

try:
    picture_url = url  # 网页地址
    InitiateId = url.split('=')[1]  # 用InitiateId作为图片文件名
    driver = webdriver.Chrome(
        r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")  # 自己现在并放到指定目录，需要自己修改

    driver.get(picture_url)
    driver.maximize_window()

    time.sleep(2)  # 延迟2秒

    driver.get_screenshot_as_file('C:\\Users\\Administrator\\Desktop\\' + InitiateId + '.png')  # 将截下的图保存到桌面
    driver.close()

    print("%s.png：截图成功！！！" % picture_url)
except BaseException as msg:
    print(msg)
