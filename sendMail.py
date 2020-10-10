# -*- coding: utf-8 -*-
# @Time : 2020/3/7 20:08
# @File : sendMail.py
# @Author : WeiSanJIn
# @Software: PyCharm

import smtplib
from email.mime.text import MIMEText
import time


def sendEmails(url, Email):
    """
    :param url: 打开成功后的分享链接
    :param Email:  收件方邮箱
    """
    # 登陆邮箱
    '''
        本地测试使用25端口 部署到服务器使用465端口
        sent = smtplib.SMTP()
        sent.connect('smtp.qq.com', 25)
    '''
    sent = smtplib.SMTP_SSL()
    sent.connect('smtp.qq.com', 465)

    print('邮件服务器:'+str(url)+'   收件人：'+str(Email))

    mail_name = "1162335221@qq.com"  # 发送人邮箱地址
    mail_password = "WeiSanJIn"  # 注意：这里不是密码，而应该填写授权码！！
    sent.login(mail_name, mail_password)  # 登陆
    # 编辑邮件内容
    to = [Email]  # 收件人邮箱地址
    mail_msg = '<p style="color: brown;font-size: 50px;text-align: center;">如果你的体温不正常，记得及时报告辅导员</p><h2 style="text-align: center;"><a href="' + url + '">' + time.strftime("%Y-%m-%d", time.localtime()) + '闽江学院易班疫情每日健康登记表</a></h2>'+'<div style="font-size: 20px;width: 60%;margin-left: 20%;margin-top: 100px;"><dl><dt><h3>注意事项</h3></dt><dd><h5 style="color: red;">1. 如果你的体温不正常，记得及时报告辅导员</h5></dd> <dd><h5>2. 当日登记表的数据是由程序动态获取前一天打卡登记表的内容</h5></dd><dd><h5>3. 如若表单更新请手动填写，第二天程序将恢复正常！</h5>'+'</dd><dd><h5>4. 如若不想再收到此通知邮件，程序任然为您每日打卡，请回复【退订】</h5></dd>'+'<dd><h5>5. 如若修改密码，重新编辑 “ 易班账号-密码-收件邮箱(可为空) ” 到本邮箱</h5></dd> </dl></div>'

    content = MIMEText(mail_msg, 'html', 'utf-8')  # 正文内容
    content['Subject'] = time.strftime("%Y-%m-%d", time.localtime()) + '　　易班每日健康打卡'  # 邮件标题
    content['From'] = mail_name  # 发件人
    content['To'] = ' , '.join(to)  # 收件人，用逗号连接多个邮件，实现群发

    # 发送邮件
    try:
        sent.sendmail(mail_name, to, content.as_string())  # 3个参数 发送人，收件人，邮件内容
        # 格式化成2016-03-20 11:45:39形式
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '　　邮件发送成功')

        sent.close()
    except smtplib.SMTPException:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '　　邮件发送失败')