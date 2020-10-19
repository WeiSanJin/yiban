# -*- coding: utf-8 -*-
# @Time :2020/3/7 18:45
# @File : testSuccess.py
# @Author : WeiSanJIn
# @Software: PyCharm
from getInitiateId import getInitiateId, latestShareUrl
from sendMail import sendEmails
from yiban import YiBan
from yiban.config import url


if __name__ == '__main__':
    # 单用户登录测试
    yb = YiBan('13888888888', 'WeiSanJin')
    if yb.login() is None:
        print("帐号或密码错误")
    result_auth = yb.auth()

    UncompletedList = yb.getUncompletedList()
    print('UncompletedList:'+str(UncompletedList))
    if not UncompletedList.get('data'):
        print('未打卡列表：'+str(UncompletedList.get('data')))
    else:
        # TaskId='bd412dff34d36392273f64753d3559fa'
        TaskId = UncompletedList.get('data')
        print('TaskId'+str(TaskId))
        TaskDetail = yb.getTaskDetail(TaskId)
        print('\n' + "未打卡的任务:"+str(TaskDetail))

    taskList = yb.taskList()
    print('\n' + "任务列表："+str(taskList))

    CompletedList = yb.getCompletedList()
    print('\n' + "已打卡的列表:")
    print(CompletedList.get('data'))

    print('\n' + "校本化列表:")
    print(result_auth.get('data'))

    Form = yb.getForm()
    print('\n' + "getForm:")
    print(Form.get('data'))

    InitiateId = url.split('=')[1]
    print("InitiateId"+InitiateId)
    if InitiateId:
        ShareUrl = yb.getShareUrl(InitiateId)
        print('\n' + "转发审批表单:")
        print(ShareUrl.get('data')['uri'])

        print('\n' + 'getFormData：')
        FormData = yb.getFormData(InitiateId)
        # print(FormData.get('data')['Initiate']['FormDataJson'])

    # 邮件服务器测试
    # sendEmails('http://www.baidu.com', '1162335221@qq.com')

    getInitiateId(yb, 2)

    latestShareUrl(yb)
