#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/7/14

import os
import sys
import socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)

# 下载文件保存路径
DOWNLOAD_PATH = os.path.join(BASE_DIR, 'download')

# 共享文件路径
UPLOAD_PATH = os.path.join(BASE_DIR, 'share')

SOCKET_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
BIND_HOST = '127.0.0.1'
BIND_PORT = 9000
SERVER_ADDRESS = (BIND_HOST, BIND_PORT)
BACKLOG = 5
BUFFER_SIZE = 8192
ENCODING = 'utf-8'

STATUS_CODE ={
    100: "新用户创建成功!",
    101: "该用户已存在!",
    200: "登录成功!",
    201: "用户名或密码错误!",
    300: "文件不存在!",
    301: "文件存在, 即将传输!",
    302: "磁盘空间不足, 无法上传!",
    303: "等待上传...",
    400: "文件夹创建成功!",
    401: "文件夹已存在!",
    500: "文件夹删除成功!",
    501: "文件夹删除失败!",
    600: "目录切换成功!",
    601: "目录切换失败!",
    }