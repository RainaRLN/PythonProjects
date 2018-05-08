#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/5/1

from core import manage
from core import user


def run():
    while True:
        login_type = input("1 用户登录\n2 管理员登录\n>>> ")
        if login_type == '1':
            user.user_run()  # 进入用户操作界面
        elif login_type == '2':
            manage.admin_run()  # 进入管理员操作界面
        else:
            print("\033[31;1m无效输入\033[0m")
