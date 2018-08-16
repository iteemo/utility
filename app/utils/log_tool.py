#!/usr/bin/python
# -*- coding: UTF-8 -*-

from get_dvd_conf import get_config
import threading,logging,logging.handlers,logging.config,sys,os,time
reload(sys)
sys.setdefaultencoding('utf8')

# 设置日志的输出格式
# 可使用范围：
# %(name)s Logger的名字
# %(levelno)s 数字形式的日志级别
# %(levelname)s 文本形式的日志级别
# %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
# %(filename)s 调用日志输出函数的模块的文件名
# %(module)s 调用日志输出函数的模块名|
# %(funcName)s 调用日志输出函数的函数名|
# %(lineno)d 调用日志输出函数的语句所在的代码行
# %(created)f 当前时间，用UNIX标准的表示时间的浮点数表示|
# %(relativeCreated)d 输出日志信息时的，自Logger创建以来的毫秒数|
# %(asctime)s 字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒
# %(thread)d 线程ID。可能没有
# %(threadName)s 线程名。可能没有
# %(process)d 进程ID。可能没有
# %(message)s 用户输出的消息

class LogsTool(object):

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # 单例设计是在这里实现的
        if len(args) != 1:
            raise Exception('创建类参数错误')

        with LogsTool._instance_lock:
            if not hasattr(LogsTool, "key_world"):
                LogsTool.key_world = {}
                LogsTool.key_world[args[0]] = object.__new__(cls)
            else:
                if not LogsTool.key_world.has_key(args[0]):
                    LogsTool.key_world[args[0]] = object.__new__(cls)

        return LogsTool.key_world[args[0]]

    def __init__(self, keyword):
        with LogsTool._instance_lock:
            if not hasattr(self,"logging_tmp"):
                self.manage(keyword)


    def manage(self, keyword):
        if get_config('logconfig', 'path') == "":
            project_path = os.path.dirname(os.path.abspath(__file__))
            logs_path = project_path.replace("app/utils", "logs")

        else:
            logs_path = get_config('logconfig', 'path')

        log_file = "%s/%s.log" % (logs_path, keyword)

        tmp = logging.getLogger(log_file)

        handler = logging.handlers.TimedRotatingFileHandler(
                        log_file,
                        when=get_config('logconfig', 'time_type'),
                        interval=int(get_config('logconfig', 'time_count')),
                        backupCount=int(get_config('logconfig', 'log_max')),
                        encoding='UTF-8')

        handler.suffix = "backup_%Y%m%d_%H-%M-%S.log"

        logging_format = logging.Formatter(
                '[%(levelname)s] [%(asctime)s] [%(message)s]')

        handler.setFormatter(logging_format)

        tmp.setLevel(get_config('logconfig', 'least').upper())
        tmp.addHandler(handler)

        self.logging_tmp = tmp

    def get_instance(self):
        return self.logging_tmp
