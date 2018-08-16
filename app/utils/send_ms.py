#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests, json

'''
这个函数用来发送邮件
name：收件人
title：标题
body：正文，可以带有转义字符
'''
def __mail(name, title, body):
    email_url = 'http://yun.ops.vyohui.com/api/dvdmail'

    email_info = {'to': name+"@davdian.com",
            'sub': title,
            'cont': body,
            'mtype': 'text/plain',
            'from': 'monitor'
            }

    email_status = requests.post(email_url,data=email_info)
    s = json.loads(email_status.text)

    if email_status.status_code == 200:
        if len(s['Information']) == 0:
            message = '发送成功'
            return True, message
        else:
            message = s['Information']
            return False,message
    else:
        message = "email_url is error"
        return False,message

'''
这个函数用来发送短信和微信
address：发微信填写名字拼音，发短信填写手机号
content：发送内容，可以带有转义字符
'''

def __message(address,content):
    url = ''

    if isinstance(address,str):
        url = 'http://yun.ops.vyohui.com/api/dvdim'
    else:
        url = 'http://yun.ops.vyohui.com/api/dvdsms'


    message_info = {'tos': address,
                    'content': content
                  }

    message_status = requests.post(url,data=message_info)
    s = json.loads(message_status.text)

    if message_status.status_code == 200:
        if isinstance(address,str):
            if len(s['Information'][0]['invaliduser']) == 0 and s['Information'][0]['errcode'] ==0:
                message = '发送成功'
                return True, message
        else:
            if len(s['Information'][0]['RequestId']) !=0:
                message = '发送成功'
                return True, message
    return False, message_status.text

'''
群发邮件
'''
def send_mail(name_list,tatil,body):
    for i in name_list:
        __mail(i,tatil,body)
    return True

def send_message(address_list,content):
    for i in address_list:
        __message(i,content)
    return True
