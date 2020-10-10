# -*- coding: utf-8 -*-
# @Time : 2020/3/7 19:42
# @File : __init__.py
# @Author : WeiSanJIn
# @Software: PyCharm

import re
import time
import requests


class YiBan:
    WFId = "e416fbced8945a7f6811d50c1563adc0"  # 疫情表单：固定表单值固定 每个大学可能不一样需要自行抓包 此处为闽江学院
    CSRF = 'a6b057f9a934b7d1b652fba42490297f'  # 固定头 无需更改
    COOKIES = {"csrf_token": CSRF}  # 固定cookie 无需更改
    HEADERS = {"Origin": "https://c.uyiban.com", "User-Agent": "yiban"}  # 固定头 无需更改

    def __init__(self, account, passwd):
        self.account = account
        self.passwd = passwd
        self.session = requests.session()

    def request(self, url, method="get", params=None, cookies=None):
        if method == "get":
            req = self.session.get(url, params=params, timeout=10, headers=self.HEADERS, cookies=cookies)
        else:
            req = self.session.post(url, data=params, timeout=10, headers=self.HEADERS, cookies=cookies)
        try:
            return req.json()
        except:
            return None

    # 用户登录
    def login(self):
        params = {
            "account": self.account,
            "ct": 2,
            "identify": 0,
            "v": "4.7.4",
            "passwd": self.passwd
        }
        r = self.request(url='https://mobile.yiban.cn/api/v2/passport/login', params=params)

        if r is not None and str(r["response"]) == "100":
            self.access_token = r["data"]["access_token"]
            self.name = r["data"]["user"]["name"]
            print('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  登录成功：' + str(self.name))
            return r
        else:
            print(self.account+"帐号或密码错误,请确认账号密码密码无误后重试")
            return None

    # 校本化
    def auth(self):
        location = self.session.get("http://f.yiban.cn/iapp/index?act=iapp7463&v=%s" % self.access_token,
                                    allow_redirects=False).headers["Location"]
        verifyRequest = re.findall(r"verify_request=(.*?)&", location)[0]

        return self.request(
            "https://api.uyiban.com/base/c/auth/yiban?verifyRequest=%s&CSRF=%s" % (verifyRequest, self.CSRF),
            cookies=self.COOKIES)

    # 未打卡的任务
    def getUncompletedList(self):
        return self.request("https://api.uyiban.com/officeTask/client/index/uncompletedList?CSRF=%s" % self.CSRF,
                            cookies=self.COOKIES)

    # 已打卡的列表
    def getCompletedList(self):
        return self.request("https://api.uyiban.com/officeTask/client/index/completedList?CSRF=%s" % self.CSRF,
                            cookies=self.COOKIES)

    # 我的任务
    def getTaskDetail(self, taskId):
        return self.request(
            "https://api.uyiban.com/officeTask/client/index/detail?TaskId=%s&CSRF=%s" % (taskId, self.CSRF),
            cookies=self.COOKIES)

    # 点击【消息】 跳转 【任务列表】
    def taskList(self):
        return self.request(
            "https://api.uyiban.com/system/Common/Message/list/1?CSRF=%s" % (self.CSRF),
            cookies=self.COOKIES)

    # 学生每日健康打卡（2稿）
    def getForm(self):
        return self.request(
            "https://api.uyiban.com/workFlow/c/my/form/%s?CSRF=%s" % (self.WFId, self.CSRF),
            cookies=self.COOKIES)

    # 退出登录
    def logout(self):
        return self.request("https://mobile.yiban.cn/api/v1/passport/logout?access_token=%s&access_token=%s" % (
        self.access_token, self.access_token),
                            cookies=self.COOKIES)

    def getFormData(self, initiateId):
        return self.request(
            "https://api.uyiban.com/workFlow/c/work/show/view/%s?CSRF=%s" % (initiateId, self.CSRF),
            cookies=self.COOKIES)

    # 提交表单
    def submit(self, data, extend):
        params = {
            "data": data,
            "extend": extend
        }
        return self.request(
            "https://api.uyiban.com/workFlow/c/my/apply/%s?CSRF=%s" % (self.WFId, self.CSRF), method="post",
            params=params,
            cookies=self.COOKIES)

    # 获取分享链接
    def getShareUrl(self, initiateId):
        return self.request(
            "https://api.uyiban.com/workFlow/c/work/share?InitiateId=%s&CSRF=%s" % (initiateId, self.CSRF),
            cookies=self.COOKIES)
