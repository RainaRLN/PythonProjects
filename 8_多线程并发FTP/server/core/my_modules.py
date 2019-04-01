#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2019/1/14

import hashlib
import json
import os
import math

INFO = "INFO"
ERROR = "ERROR"
WARNING = "WARNING"
B, KB, MB, GB = 0, 1, 2, 3


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


def print_log(level, msg):  # 高亮提示
    if level == "INFO":
        format_msg = "\033[32;1m{}\033[0m"
    elif level == "WARNING":
        format_msg = "\033[35;1m{}\033[0m"
    else:  # level == "ERROR"
        format_msg = "\033[31;1m{}\033[0m"
    print(format_msg.format(msg))


def hex_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def save_db(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)


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


def get_file_size(file_path, mode=0, size=0):
    for root, dirs, files in os.walk(file_path):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size/math.pow(1024, mode)
