# -*- coding: utf-8 -*-
# @Time :2020/3/7 14:45
# @File : submit.py
# @Author : WeiSanJIn
# @Software: PyCharm
import json
import re
import userData
from sendMail import sendEmails
from getInitiateId import getInitiateId, latestShareUrl
from yiban import YiBan

if __name__ == '__main__':
    for user in userData.data:
        yb = YiBan(user['ACCOUNT'], user['PASSWD'])
        # 登录判断
        if yb.login() is None:
            # exit(1)
            continue
        # 校本化列表
        result_auth = yb.auth()
        data_url = result_auth["data"].get("Data")
        if data_url is not None:  # 授权过期
            print("授权过期")
            print("访问授权网址")
            result_html = yb.session.get(url=data_url, headers=yb.HEADERS,
                                         cookies={"loginToken": yb.access_token}).text
            re_result = re.findall(r'input type="hidden" id="(.*?)" value="(.*?)"', result_html)
            print("输出待提交post data")
            print(re_result)
            post_data = {"scope": "1,2,3,"}
            for i in re_result:
                post_data[i[0]] = i[1]
            print("进行授权确认")
            usersure_result = yb.session.post(url="https://oauth.yiban.cn/code/usersure",
                                              data=post_data,
                                              headers=yb.HEADERS, cookies={"loginToken": yb.access_token})
            if usersure_result.json()["code"] == "s200":
                print("授权成功！")
            else:
                print("授权失败！")
            print("尝试重新二次登录")
            yb.auth()
        # 获取最新的表单连接,返回最终提交的表单数据
        form_data = getInitiateId(yb, 2)

        # 获取待打卡列表
        all_task = yb.getUncompletedList()
        if len(all_task["data"]) == 0:
            print("没有待完成的打卡任务")
        for i in all_task["data"]:
            # print(i)
            if (i["Title"] == '11月5-6日社区晚值班宿舍检查违纪学生反馈'):
                print("WeiSanJin.submit       ：没有待完成的打卡任务!" + '\n')
                break
            task_detail = yb.getTaskDetail(i["TaskId"])["data"]
            if task_detail["WFId"] != yb.WFId:
                print("表单已更新,得更新程序了")
                print("WeiSanJin：1. 查看WFId 是否已经更新")
                print("WeiSanJin：2. 可以尝试看看打开列表中有无任务卡住，进行跳过无关任务(52-54行)")
                exit()
            ex = {"TaskId": task_detail["Id"],
                  "title": "任务信息",
                  "content": [{"label": "任务名称", "value": task_detail["Title"]},
                              {"label": "发布机构", "value": task_detail["PubOrgName"]},
                              {"label": "发布人", "value": task_detail["PubPersonName"]}]}
            submit_result = yb.submit(form_data, json.dumps(ex, ensure_ascii=False))
            if submit_result.get('code') == 0:
                print(task_detail["Title"] + " 打卡成功")
                # share_url = yb.getShareUrl(submit_result["data"])["data"]["uri"]
                # 防止链接失效,再次获取分享链接
                ShareUrl = latestShareUrl(yb)
                # 发送邮件
                sendEmails(ShareUrl, user['Email'])
                # 打卡成功后将分享链接写入config
                with open('config.txt', 'w') as f:
                    f.write(ShareUrl)
                print("分享的链接为: " + ShareUrl)

