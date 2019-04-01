#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5


def print_menu(menu):
    for i in menu:
        print(i, menu[i][0])


def check_choice(limit):
    choice = input(">>> ")
    if choice.isdigit() and int(choice) in range(0, limit):
        return choice
    else:
        print("无效输入!")
        check_choice(limit)
