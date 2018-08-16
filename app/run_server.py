#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from datetime import timedelta


# 导入 flask的Flask模块路由功能
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)


# 用户相关api
from class_example.view import test
app.register_blueprint(test)


if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8888,debug=True)
