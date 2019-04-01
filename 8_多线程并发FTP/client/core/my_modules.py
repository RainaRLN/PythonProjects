#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/7/16

from prettytable import PrettyTable
from time import sleep
import os

INFO = "INFO"
ERROR = "ERROR"
WARNING = "WARNING"


def print_menu(menu):
    for i in menu:
        print(i, menu[i][0])


def check_choice(limit):
    choice = input(">>> ")
    if choice.isdigit() and int(choice) in range(0, limit):
        return choice
    else:
        print("无效输入!")
        choice = check_choice(limit)
    return choice


def print_log(level, msg):  # 高亮提示
    if level == "INFO":
        format_msg = "\033[32;1m{}\033[0m"
    elif level == "WARNING":
        format_msg = "\033[35;1m{}\033[0m"
    else:  # level == "ERROR"
        format_msg = "\033[31;1m{}\033[0m"
    print(format_msg.format(msg))


def print_table(head_list, row_list):
    table = PrettyTable(head_list)
    for row in row_list:
        table.add_row(row)
    print(table)


def bar_print(recv_size, full_size, mode='d'):
    if mode == 'u':
        bar = "<上传进度: {:.2f}%> {}{}"
    else:
        bar = "<下载进度: {:.2f}%> {}{}"
    b = int(recv_size * 25 / full_size)
    w = 25 - b
    print('\r' + bar.format(recv_size/full_size*100, '█'*b, '░'*w), end='')
    sleep(0.2)


def rename_file(path, old, new):
    old_name = os.path.join(path, old)
    new_name = os.path.join(path, new)
    try:
        os.rename(old_name, new_name)
    except FileExistsError:
        for i in range(20):
            name_list = new.split('.')
            name_list[0] += '({}).'.format(i+1)
            new_name = os.path.join(path, ''.join(name_list))
            if not os.path.isfile(new_name):
                os.rename(old_name, new_name)
                return
