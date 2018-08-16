#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 导入DBUtils模版
from DBUtils.PooledDB import PooledDB
# 这里使用的是PooledDB方式，具体可参考官网：https://cito.github.io/w4py-olde-docs/Webware/DBUtils/Docs/UsersGuide.html

# 导入mysql驱动
import mysql.connector, threading, traceback
from get_dvd_conf import get_config
# 导入log驱动
from log_tool import LogsTool


class MysqlTool(object):
    instance_lock = threading.Lock()

    def __init__(self, config_name):

        self.config_name = config_name

        self.log_sql = LogsTool('sql').get_instance()

        with self.instance_lock:
            if not hasattr(self, "_pool"):
                self._get_con()

        self._conn = self._pool.connection()
        self._cursor = self._conn.cursor()

    def __new__(cls, *args, **kwargs):
        # 单例设计是在这里实现的
        if len(args) != 1:
            raise Exception('创建类参数错误')

        with MysqlTool.instance_lock:
            if not hasattr(MysqlTool, "config"):
                MysqlTool.config = {}
                MysqlTool.config[args[0]] = object.__new__(cls)
            else:
                if not MysqlTool.config.has_key(args[0]):
                    MysqlTool.config[args[0]] = object.__new__(MysqlTool)

        return MysqlTool.config[args[0]]

    def _get_con(self):
        '''
            配置说明：
                dbapi:数据库接口
                mincached:启动时开启的空连接数量
                maxcached:连接池最大可用连接数量
                maxshared:连接池最大可共享连接数量
                maxconnections:最大允许连接数量
                blocking:达到最大数量时是否阻塞
                maxusage:单个连接最大复用次数
                setsession:用于传递到数据库的准备会话
        '''
        try:
            self._pool = PooledDB(creator=mysql.connector, mincached=2, maxcached=5,
                                  host=get_config(self.config_name, 'dbhost'),
                                  port=int(get_config(self.config_name, 'dbport')),
                                  user=get_config(self.config_name, 'dbuser'),
                                  passwd=get_config(self.config_name, 'dbpasswd'),
                                  database=get_config(self.config_name, 'dbname'),
                                  charset=get_config(self.config_name, 'dbcharset'))
        except mysql.connector.Error as e:
            self.log_sql.error(
                '[The MySQL Connect failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config_name, e,
                                                                                          traceback.format_exc()))
        else:
            self.log_sql.info('[The MySQL Connect success] [Config:{}]'.format(self.config_name))

    def close(self, isEnd=1):
        '''
            释放连接池资源
        '''
        self._cursor.close()
        self._conn.close()

    def _query(self, sql, param=None):
        # 默认执行的方法
        try:
            if param is None:
                self._cursor.execute(sql)
            else:
                self._cursor.execute(sql, param)
            self._conn.commit()

            self.log_sql.info('[Exexute sql success!] [config:{}] [sql:{}]'.format(self.config_name, sql))

            return True

        except mysql.connector.Error as e:
            self.log_sql.error(
                '[Exexute sql failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config_name, e,
                                                                                    traceback.format_exc()))

            return False

    def get_insertId(self):
        '''
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        '''
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def update_db(self, sql, param=None):
        # sql:UPDATE tablename SET *** WHERE ***

        return self._query(sql, param)

    def delete_db(self, sql, param=None):
        # sql:DELETE FROM *** WHERE ***

        return self._query(sql, param)

    def alter_db(self, sql, param=None):
        # sql:ALTER TABLE *** DROP/ADD/MODIFY/CHANGE ***

        return self._query(sql, param)

    def select_all(self, sql, param=None):
        # 如果sql执行成功，返回的是结构集，sql语句有问题返回false
        try:
            self._cursor.execute(sql, param)
            result = self._cursor.fetchall()

            self.log_sql.info('[Exexute sql success!] [config:{}] [sql:{}]'.format(self.config_name, sql))

            return result

        except mysql.connector.Error as e:
            self.log_sql.error(
                '[Exexute sql failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config_name, e,
                                                                                    traceback.format_exc()))
            return False

    def select_one(self, sql):
        # 如果sql执行成功，返回的是结构集，sql语句有问题返回信息
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchone()

            self.log_sql.info('[Exexute sql success!] [config:{}] [sql:{}]'.format(self.config_name, sql))

            return result

        except mysql.connector.Error as e:

            self.log_sql.error(
                '[Exexute sql failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config_name, e,
                                                                                    traceback.format_exc()))

            return False

    def insert_one(self, sql):
        # 执行一条添加语句
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            self.log_sql.info('[Exexute sql success!] [config:{}] [sql:{}]'.format(self.config_name, sql))

            return True
        except mysql.connector.Error as e:
            self.log_sql.error(
                '[Exexute sql failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config_name, e,
                                                                                    traceback.format_exc()))
            return False

    def insert_many(self, sql, values):
        # 执行多条添加语句
        '''
        实例：
            sql='insert into white_list(name) value(%s)'
            values = ((aa,),(bb,))
            self._cursor.executemany(sql, values)
        '''
        try:
            self._cursor.executemany(sql, values)
            self._conn.commit()
            self.log_sql.info('[Exexute sql success!] [config:{}] [sql:{}]'.format(self.config_name, sql))
            return True
        except mysql.connector.Error as e:
            self.log_sql.error(
                '[Exexute sql failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config_name, e,
                                                                                    traceback.format_exc()))
            return False
