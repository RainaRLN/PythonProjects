#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/5/2

"""
atm相关操作函数
"""

from prettytable import PrettyTable
from core import logger
import os
import time
import json

path = os.path.abspath('..')

SAVE = "存款"
WITHDRAW = "取款"
TRANS = "转账"
PAY = "支付"
GET = "收到转账"

log_msg = "account: %s  action: %s amount: %d"


# 用户认证
def authentification(func):
    def inner(acc, money):
        while True:
            password = input("请输入支付密码:")
            f = open(path + r"\db\users.json", "r")
            account_dicts = json.load(f)
            f.close()
            for i in account_dicts:
                if i['id'] == acc['id'] and i['password'] == password:
                    print("\033[32;1m认证成功\033[0m")
                    break
            else:
                print("\033[31;1m密码错误\033[0m")
                logger.log("account").error("account: %s  action: authentification  error: password error" % acc['id'])
                continue
            return func(acc, money)
    return inner


def save_db(acc):
    """
    保存用户信息
    :param acc: 用户信息字典
    :return: None
    """
    f = open(path + r"\db\users.json", "r")
    account_dicts = json.load(f)
    for i in account_dicts:
        if i["id"] == acc['id']:
            i.update(acc)
    f.close()
    f = open(path + r"\db\users.json", "w")
    json.dump(account_dicts, f)
    f.close()


def save_check(acc, opt_type, charge, left):
    """
    保存用户账单
    :param acc: 用户信息字典
    :param opt_type: 账单类型: SAVE->存款 WITHDRAW->取款 TRANS->转账 PAY->支付 GET->收到转账
    :param charge: 账单金额
    :param left: 余额
    :return: None
    """
    this_time = time.strftime("%Y-%m-%d %H:%M:%S")
    f = open(path + "\db\\" + acc['id'] + ".txt", "r+", encoding="utf-8")
    f.read()
    f.write("%s: %s%d元, 余额%d元\n" % (this_time, opt_type, int(charge), int(left)))
    f.close()


def account_info(acc):
    """
    打印用户信息
    :param acc: 用户信息字典
    :return: None
    """
    x = PrettyTable(header=False)
    for i in acc:
        x.add_row([i, acc[i]])
    print(x)


def top_up(acc):
    """
    存款
    :param acc: 用户信息字典
    :return: None
    """
    while True:
        money = input("请输入存款金额: ")
        if money.isdigit():
            acc['balance'] += int(money)
            save_check(acc, SAVE, money, acc['balance'])
            save_db(acc)
            print("\033[32;1m操作成功,当前余额为%s元\033[0m" % acc['balance'])
            logger.log("transactions").info(log_msg % (acc['id'], 'top up', int(money)))
            return
        else:
            print("\033[31;1m请输入数字\033[0m")


def withdraw(acc):
    """
    取款
    :param acc: 用户信息字典
    :return: None
    """
    while True:
        money = input("请输入提款金额: ")
        if money.isdigit():
            if acc['balance'] >= int(money):
                fee = 0.05 * int(money)  # 手续费5%
                if fee < 1:  # 不足一元按一元收手续费
                    fee = 1
                acc['balance'] -= int(money)
                save_check(acc, WITHDRAW, money, acc['balance'])
                save_db(acc)
                print("\033[32;1m成功提现%d元(手续费%d元),当前余额为%s元\033[0m" % ((int(money)-fee), fee, acc['balance']))
                logger.log("transactions").info(log_msg % (acc['id'], 'withdraw', int(money)))
                return
            else:
                print("\033[31;1m余额不足\033[0m")
                logger.log("transactions").error(
                    log_msg % (acc['id'], 'withdraw', int(money)) + "  error: balance not enough")
        else:
            print("\033[31;1m请输入数字\033[0m")


def trans_money(acc, obj_acc):
    """
    转账
    :param acc: 转账发起用户的信息字典
    :param obj_acc: 转账对象的用户字典
    :return: None
    """
    while True:
        money = input("请输入转账金额: ")
        if money.isdigit():
            if acc['balance'] >= int(money):
                acc['balance'] -= int(money)
                obj_acc['balance'] += int(money)
                save_check(acc, TRANS, money, acc['balance'])
                save_check(obj_acc, GET, money, obj_acc['balance'])
                save_db(acc)
                save_db(obj_acc)
                print("\033[32;1m转账成功\033[0m")
                logger.log("transactions").info(log_msg % (acc['id'], 'transfer money', int(money)))
                return
            else:
                print("\033[31;1m余额不足\033[0m")
                logger.log("transactions").error(
                    log_msg % (acc['id'], 'transfer money', int(money)) + "  error: balance not enough")
        else:
            print("\033[31;1m请输入数字\033[0m")


@ authentification
def pay_money(acc, money):
    """
    支付函数
    :param acc: 用户信息字典
    :param money: 需支付的金额
    :return: 1->支付成功 0->支付失败
    """
    if acc['balance'] >= int(money):
        acc['balance'] -= money
        save_check(acc, PAY, money, acc['balance'])
        save_db(acc)
        logger.log("transactions").info(log_msg % (acc['id'], 'shopping', int(money)))
        return 1
    else:
        logger.log("transactions").error(log_msg % (acc['id'], 'shopping', int(money)) + "  error: balance not enough")
        return 0


def pay_check(acc):
    """
    打印用户账单
    :param acc: 用户信息字典
    :return: None
    """
    f = open(path + "\db\\" + acc['id'] + ".txt", "r", encoding="utf-8")
    data = f.read()
    print(data)
