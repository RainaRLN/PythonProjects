#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/5/5

"""
管理员入口
"""

import os
import json
import time
from prettytable import PrettyTable
from conf.settings import USER_DICTS
from conf.settings import USER_ID_LIST
from conf.settings import ADMIN_DICTS
from conf.settings import USER_PATH
from conf.settings import BASE_DIR


def get_check_path(user_id):
    """
    获取用户账单文件路径
    :param user_id: 用户id
    :return: 用户账单文件路径
    """
    return os.path.abspath(os.path.join(BASE_DIR, "db", user_id + ".txt"))


def save_db():
    """
    用户信息
    :return: None
    """
    file = open(USER_PATH, "w")
    json.dump(USER_DICTS, file)
    file.close()


def save_new_db(new_user_dict):
    """
    保存新创建的用户信息
    :param new_user_dict:
    :return:
    """
    USER_DICTS.append(new_user_dict)
    USER_ID_LIST.append(new_user_dict['id'])
    # file = open(path + "\db\\" + new_user_dict['id'] + ".txt", "w", encoding="utf-8")  # 流水账文件
    path = get_check_path(new_user_dict['id'])
    print("path:", path)
    file = open(path, "w", encoding="utf-8")  # 流水账文件
    file.close()
    save_db()


def account_info(user_id):
    """
    打印用户信息
    :param user_id: 要查看信息的用户id
    :return: None
    """
    if user_id in USER_ID_LIST:
        index = USER_ID_LIST.index(user_id)
        x = PrettyTable(header=False)
        for k in USER_DICTS[index]:
            x.add_row([k, USER_DICTS[index][k]])
        print(x)
    else:
        print("\033[31;1m用户不存在\033[0m")


def create_user(new_id):
    """
    创建新用户
    :param new_id: 新用户id
    :return: None
    """
    if new_id in USER_ID_LIST:
        print("\033[31;1m用户已存在\033[0m")
    else:
        print("\033[32;1m请输入新用户的信息\033[0m")
        password = input("password: ")
        credit = balance = ''
        while not credit.isdigit():
            credit = input("credit(需为数字): ")
        while not balance.isdigit():
            balance = input("balance(需为数字): ")
        new_user_dict = {
            'id': new_id,
            'password': password,
            'credit': int(credit),
            'balance': int(balance),
            'enroll_date': time.strftime("%Y-%m-%d"),
            'status': 3
        }
        save_new_db(new_user_dict)
        print("\033[32;1m已添加用户: %s\033[0m" % new_id)
        account_info(new_id)


def del_user(user_id):
    """
    删除用户
    :param user_id: 要删除的用户id
    :return: None
    """
    if user_id in USER_ID_LIST:
        index = USER_ID_LIST.index(user_id)
        del USER_DICTS[index]
        USER_ID_LIST.remove(user_id)
        # os.remove(path + "\db\\" + user_id + ".txt")
        os.remove(get_check_path(user_id))
        save_db()
        print("\033[32;1m已删除用户: %s\033[0m" % user_id)
    else:
        print("\033[31;1m用户不存在\033[0m")


def change_db(user_id):
    """
    修改用户信息
    :param user_id: 要修改用户的id
    :return: None
    """
    if user_id in USER_ID_LIST:
        index = USER_ID_LIST.index(user_id)
        account_info(user_id)
        item = input("请输入要修改的项(password, credit, balance)\n>>> ")
        if item in ["password", "credit", "balance"]:
            new_info = input("请输入要修改成的内容\n>>> ")
            if item == 'credit' or item == 'balance':
                if new_info.isdigit():
                    new_info = int(new_info)
                else:
                    print("\033[31;1m请输入数字\033[0m")
                    return
            USER_DICTS[index][item] = new_info
            save_db()
            print("\033[32;1m修改成功\033[0m")
            account_info(user_id)
        else:
            print("\033[31;1m输入项不存在, 或该项不支持修改\033[0m")
    else:
        print("\033[31;1m用户不存在\033[0m")


def lock_account(user_id):
    """
    锁定用户(status改为-1)
    :param user_id: 要锁定用户的id
    :return: None
    """
    if user_id in USER_ID_LIST:
        index = USER_ID_LIST.index(user_id)
        USER_DICTS[index]['status'] = -1
        save_db()
        print("\033[32;1m用户%s已锁定\033[0m" % user_id)
    else:
        print("\033[31;1m用户不存在\033[0m")


def login_succeed():
    """
    管理员登录函数
    :return: 登录成功返回True
    """
    while True:
        # 输入管理员用户名密码
        admin_name = input("username: ")
        password = input("password: ")
        # 验证用户名密码
        for admin in ADMIN_DICTS:
            if admin_name == admin['id'] and password == admin['password']:
                print("\033[31;1m登录成功!\033[0m")
                return True
        else:
            print("\033[41;1m用户名或密码错误,请重试\033[0m")


option = """
请选择下续操作:
    1 创建用户
    2 删除用户
    3 冻结用户
    4 修改用户信息
    5 查看用户信息
    Q 退出
"""
option_dict = {
        '1': create_user,
        '2': del_user,
        '3': lock_account,
        '4': change_db,
        '5': account_info,
    }


def admin_run():
    if login_succeed():
        while True:
            choice = input(option + ">>> ")
            if choice in option_dict:
                print("已存在的用户id: %s" % USER_ID_LIST)
                username = input("请输入要操作或添加的用户id: ")
                option_dict[choice](username)
            elif choice == 'Q' or choice == 'q':
                print("\033[31;1m已退出!\033[0m")
                exit()
            else:
                print("\033[41;1m无效输入!\033[0m")
