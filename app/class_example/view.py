#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, json,Blueprint, session
from utils.log_tool import LogsTool

test = Blueprint('test_b',__name__)

test_log = LogsTool('test')

@test.route('/',methods=['GET','POST'])
def show():

    test_log.info("这是一条日志")
    return "nihao"

