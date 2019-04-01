#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5

import os
import sys
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 数据信息路径
INFO_PATH = os.path.abspath(os.path.join(BASE_DIR, "db", "info.pk"))

# 日志文件配置
LOG_PATH = os.path.abspath(os.path.join(BASE_DIR, "logs", "system.log"))

with open(INFO_PATH, 'rb') as f:
    INFO_DICT = pickle.loads(f.read())
