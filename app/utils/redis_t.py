#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
from redis_tool import Redis_tool
r2 = Redis_tool('redisconfig_beta')

pub=r2.subscribe_t('test')

while True:
    print pub.parse_response()[2]


