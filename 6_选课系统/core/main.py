#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5

from core.interface import *
from core.my_modules import *


def login():
    login_menu = {
        '0': ['管理员视图', ManagerInterface],
        '1': ['讲师视图', TeacherInterface],
        '2': ['学员视图', StudentInterface],
    }
    print_menu(login_menu)
    print("请选择视图: ")
    choice = check_choice(3)
    interface = login_menu[choice][1]()
    obj = interface.login()
    return interface, obj


def run():
    interface, obj = login()
    interface.run(obj)
