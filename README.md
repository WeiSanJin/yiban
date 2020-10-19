# 闽江学院_自动化易班每日健康打卡

# 📇目录说明

```text
│  .gitignore
│  README.md     
|  接口说明.md          更新接口说明文档
│  submit.py           自动打卡脚本
|  sendMail.py         邮件服务功能
|  getImage.py         打卡截图功能
│  testSuccess.py      测试程序
|  userData.py         批量打卡账号信息
|  getInitiateId.py    获取表单数据
│  utils.py            工具包,完成表单数据的提取和填充
│  config.txt          打卡分享链接
└─yiban
      │  __init__.py   存放基础类
```

# 🚀安装

```shell script
git clone https://github.com/WeiSanJin/yiban.git

pip install requests
```

# 📃使用说明

#### 1. 修改配置参数

- 将userData.py下的账号密码邮箱换成自己的

#### 2. 测试是否有未打卡的任务

```shell script
python testSuccess.py
```

#### 3. 打卡

```shell script
python submit.py
```

## :hourglass_flowing_sand:服务器每天定时打卡

终端运行：`crontab -e`

定时列表：`crontab -l`

```javascript
00 17 * * * python3 yiban/submit.py >> ~/result.txt
```

```javascript
* * * * * 
*所代表的的含义
M: 分（0-59） 
H：时（0-23）
D：天（1-31）
m: 月（1-12）
d: 周（0-6） 0为星期日
```

退出并保存：<kbd>esc</kbd>+<kbd>:wq</kbd>



## 🌈参考

- https://github.com/WadeStack/yiban

## 📮联系方式

- :email: 1162335221@qq.com

