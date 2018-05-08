#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/5/8

from core import bank
from core import market
from core import logger
from conf.settings import USER_DICTS
from conf.settings import USER_ID_LIST


def transfer(acc):
    """
    调用bank的trans_money转账函数
    :param acc: 发起转账用户的信息字典
    :return: None
    """
    while True:
        obj = input("对方账户: ")  # 转账对象id
        if obj in USER_ID_LIST:
            index = USER_ID_LIST.index(obj)
            obj_acc = USER_DICTS[index]  # 转账对象信息字典
            bank.trans_money(acc, obj_acc)
            return
        else:
            print("\033[31;1m此账户不存在\033[0m")
            logger.log("transactions").error("account: %s  action: %s error: %s"
                                             % (acc['id'], 'transfer money', 'transfer object not exit'))


def logout(acc):
    """
    退出
    :param acc: 用户信息字典
    :return: None
    """
    print("\033[31;1m用户%s已退出\033[0m" % acc['id'])
    exit()


def interactive(acc):
    """
    用户操作界面
    :param acc: 用户信息字典
    :return: None
    """
    option = """
    -----------------\033[32;1m
      1 账户信息
      2 存款
      3 取款
      4 转账
      5 账单
      6 购物
      7 退出\033[0m
    -----------------
    """
    option_dict = {
        '1': bank.account_info,
        '2': bank.top_up,
        '3': bank.withdraw,
        '4': transfer,
        '5': bank.pay_check,
        '6': market.shopping,
        '7': logout
    }
    while True:
        choice = input(option + ">>> ").strip()
        if choice in option_dict:
            option_dict[choice](acc)
        else:
            print("\033[31;1m无效输入\033[0m")


def log_in(acc_dicts):
    """
    用户登录函数
    :param acc_dicts: 所有账户信息
    :return: 已登录用户信息
    """
    while True:
        # 输入用户名密码登录
        username = input("username: ").strip()
        password = input("password: ").strip()

        # 验证用户名与密码
        if username in USER_ID_LIST:
            index = USER_ID_LIST.index(username)

        else:
            print("\033[31;1m此用户不存在\033[0m")
            logger.log("account").error("action: login  error: user not exit")
            continue
        if acc_dicts[index]['status'] > 0:  # 验证是否被锁定
            if acc_dicts[index]['password'] == password:
                print("\033[31;1m登录成功!\033[0m")
                acc_data = acc_dicts[index].copy()
                del acc_data['password']
                del acc_data['status']
                acc_dicts[index]['status'] = 3
                return acc_data
            else:
                print("\033[31;1m用户名或密码错误,请重试\033[0m")
                logger.log("account").error("account: %s  action: login  error: password error" % username)
                acc_dicts[index]['status'] -= 1
        elif acc_dicts[index]['status'] == 0:  # 是否密码错误次数过多
            bank.save_db(acc_dicts[index])
            print("\033[31;1m密码错误次数过多, 账户已被锁定\n"
                  "请联系管理员解除锁定\033[0m")
            logger.log("account").error("account: %s  action: login  error: password error too many times" % username)
        else:  # status == -1, 用户被管理员所动
            print("\033[31;1m账户已被管理员锁定\n"
                  "请联系管理员解除锁定\033[0m")
            logger.log("account").error("account: %s  action: login  error: account be locked" % username)


def user_run():
    acc_data = log_in(USER_DICTS)  # 登录, 得到已登录用户信息
    interactive(acc_data)  # 进入用户操作界面
