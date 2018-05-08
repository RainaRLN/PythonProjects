#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/5/7

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)


# 管理员文件配置
MANAGE_PATH = os.path.abspath(os.path.join(BASE_DIR, "db", "admins.json"))

# 用户文件配置
USER_PATH = os.path.abspath(os.path.join(BASE_DIR, "db", "users.json"))

# 日志文件配置
LOG_PATH = os.path.abspath(os.path.join(BASE_DIR, "logs", "atm.log"))

# 管理员信息
f = open(MANAGE_PATH, "r")
ADMIN_DICTS = json.load(f)
f.close()

# 用户信息
f = open(USER_PATH, "r")
USER_DICTS = json.load(f)
f.close()

# 用户id列表
USER_ID_LIST = [user['id'] for user in USER_DICTS]

# 管理员id列表
ADMIN_ID_LIST = [user['id'] for user in ADMIN_DICTS]
