#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser
from os.path import abspath, dirname, join

def get_config(section, key):
    config = ConfigParser.ConfigParser()
    project_path = dirname(dirname(abspath(__file__)))
    project_path = project_path.replace("app", "conf/all.conf")
    config.read(project_path)
    return config.get(section, key)

