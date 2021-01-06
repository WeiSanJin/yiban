# -*- coding: utf-8 -*-
# @Time :2020/3/7 13:45
# @File : getInitiateId.py
# @Author : WeiSanJIn
# @Software: PyCharm
from utils import parse_data

def getInitiateId(yb, type):
    """
        :param yb: 实例化yb对象
        :param type:  返回数据类型0：最新表单 1：前一天表单
    """
    # 通过访问任务列表获取TaskId
    taskList = yb.taskList()
    TaskId = taskList.get('data')['list'][type]["LinkTo"].split('=')[1]
    CompletedList = yb.getTaskDetail(TaskId)
    # 我的任务
    # 对< InitiateId >进行异常捕获，寻找到最新的值
    try:
        InitiateId = CompletedList.get('data')['InitiateId']
    except KeyError:
        if TaskId == 'view&id' or InitiateId is not None:
            for i in range(10):
                TaskId = taskList.get('data')['list'][i]["LinkTo"].split('=')[1]
                if TaskId != 'view&id':
                    CompletedList = yb.getTaskDetail(TaskId)
                    InitiateId = CompletedList.get('data')['InitiateId']
                           # WeiSanJin.getInitiateId：
                    print("WeiSanJin.异常处理      ：<- InitiateId -> " + str(InitiateId))
                    break

    shareUrl = 'https://app.uyiban.com/workflow/client/#/share?initiateId=' + InitiateId

    # 防止链接失效,再次获取分享链接
    ShareUrl = yb.getShareUrl(InitiateId)

    # 将最新的分享链接写入 config.txt
    with open('config.txt', 'w') as f:
        # print('\n' + "分享链接：" + shareUrl)
        f.write(shareUrl)

    # 返回最新的表单数据
    return parse_data(shareUrl, yb)


def latestShareUrl(yb):
    """
        :param yb: 实例化yb对象
    """
    # 通过访问任务列表获取TaskId
    taskList = yb.taskList()
    TaskId = taskList.get('data')['list'][0]["LinkTo"].split('=')[1]
    if TaskId == 'view&id':
        for i in range(5):
            TaskId = taskList.get('data')['list'][i]["LinkTo"].split('=')[1]
            if TaskId != 'view&id':
                break

    CompletedList = yb.getTaskDetail(TaskId)
    InitiateId = CompletedList.get('data')['InitiateId']
    shareUrl = 'https://app.uyiban.com/workflow/client/#/share?initiateId=' + InitiateId

    # 防止链接失效,再次获取分享链接
    ShareUrl = yb.getShareUrl(InitiateId)

    # 将最新的分享链接写入 config.txt
    with open('config.txt', 'w') as f:
        # print('\n' + "分享链接：" + str(ShareUrl['data']['uri']))
        f.write(str(shareUrl))

    # 返回最新的分享链接
    print("激活分享链接：" + str(shareUrl))
    return shareUrl
