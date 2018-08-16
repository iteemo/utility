#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/16 下午5:25
# @Author  : iteemo
# @File    : mysqlutile.py
import pymysql as ps

class MysqlUtile:
    def __init__(self, host, user, password, database, charset):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.db = None
        self.curs = None
    # 数据库连接
    def open(self):
        self.db = ps.connect(host=self.host, user=self.user, password=self.password,database=self.database, charset=self.charset)
        self.curs = self.db.cursor()
    # 数据库关闭
    def close(self):
        self.curs.close()
        self.db.close()
    # 数据增删改
    def cud(self, sql):
        self.open()
        try:
            self.curs.execute(sql)
            self.db.commit()
            print("ok")
        except :
            print('cud出现错误')
            self.db.rollback()
        self.close()
    # 数据查询
    def find(self, sql):
        self.open()
        try:
            result = self.curs.execute(sql)
            self.close()
            print("ok")
            return result
        except:
            print('find出现错误')