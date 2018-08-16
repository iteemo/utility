#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis, threading, traceback
from log_tool import LogsTool
from get_dvd_conf import get_config

log_redis = LogsTool('redis')


# 目前只是简单的发布订阅模式
class Redis_tool(object):
    _instance_lock = threading.Lock()

    def __init__(self, config):
        self.config = config

        self.log_redis = LogsTool('redis').get_instance()

        with self._instance_lock:
            if not hasattr(self, '_redis_tmp'):
                self._connect()

    def __new__(cls, *args, **kwargs):
        # 单例设计是在这里实现的
        if len(args) != 1:
            raise Exception('创建类参数错误')

        with Redis_tool._instance_lock:
            if not hasattr(Redis_tool, "config_d"):
                Redis_tool.config_d = {}
                Redis_tool.config_d[args[0]] = object.__new__(cls)
            else:
                if not Redis_tool.config_d.has_key(args[0]):
                    Redis_tool.config_d[args[0]] = object.__new__(cls)
        return Redis_tool.config_d[args[0]]

    def _connect(self):
        try:
            self._pool = redis.ConnectionPool(host=get_config(self.config, 'host'),
                                              port=get_config(self.config, 'port'),
                                              password=get_config(self.config, 'password'))
            self._redis_tmp = redis.Redis(connection_pool=self._pool)

            self.log_redis.info("[The Redis Connect success] [Config:{}]".format(self.config))

        except Exception as e:
            self.log_redis.error(
                '[The Redis Connect failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config, e,
                                                                                          traceback.format_exc()))

    def publish_t(self, channel, message):
        try:
            num = self._redis_tmp.publish(channel, message)
            self.log_redis.info(
                "[Publish success] [Config:{}] [Channel:{}] [Message:{}] [Subscribe_num:{}]".format(self.config,
                                                                                                    channel, message,
                                                                                                    num))
            return True
        except Exception as e:
            self.log_redis.error(
                '[Publish failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config, e, traceback.format_exc()))
            return False

    def subscribe_t(self, channel):
        try:
            pub = self._redis_tmp.pubsub()
            pub.subscribe(channel)
            pub.parse_response()
            return pub
        except Exception as e:
            self.log_redis.error(
                '[subscribe failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config, e,
                                                                                  traceback.format_exc()))
            return False

# 发布模式
# r1 = Redis_tool()
#
# r1.publish('test','buaho')

# 订阅模式
# r2 = Redis_tool()
#
# pub=r2.subscribe('test')
#
# while True:
#
#     print pub.parse_response()[2]
