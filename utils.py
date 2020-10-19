# -*- coding: utf-8 -*-
# @Time :2020/3/9 1:42
# @File : utils.py
# @Author :WeiSanJin
# @Software: PyCharm

import json
import requests


def parse_data(url, yb):
    """
    :param url: 将分享链接的数据解析出来生成表单数据字典
    :param yb : 实例化yb对象
    :return   : 最终提交的表单数据
    """
    # 防止链接失效 再次获取分享链接
    initiateId = url.split('=')[-1]
    ShareUrl = yb.getShareUrl(initiateId)

    # 获取表单数据
    share_url = 'https://api.uyiban.com/workFlow/c/share/index?InitiateId={}&CSRF={}'.format(initiateId, yb.CSRF)
    share_res = yb.request(share_url, cookies=yb.COOKIES)
    save_data_url = share_res.get('data')['uri']
    save_data_res = requests.get(save_data_url)
    save_data = save_data_res.json()
    FormDataJson = save_data.get('Initiate')['FormDataJson']
    dict_form = {i.get('id'): i.get("value") for i in FormDataJson}
    return json.dumps(dict_form)
