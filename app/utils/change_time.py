#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def change_to_str(num):
    timestamp = num

    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

    return dt

def change_to_num(strtime):
    # 转换成时间数组
    timeArray = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)

    return int(timestamp)


