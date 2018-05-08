#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/5/3

"""
购物相关操作函数
"""
from core import bank

INFO = "INFO"
ERROR = "ERROR"
WARNING = "WARNING"

goods = [  # 商品信息
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998}
]

# 创建{商品名:价格}字典
goods_dict = {}

for item in goods:
    goods_dict[item["name"]] = item["price"]


def payment(acc, expense):
    """
    调用bank的pay_money函数支付购物车商品金额
    :param acc: 用户信息字典
    :param expense: 需支付金额
    :return: None
    """
    print_log(INFO, "代付金额为%d元,是否购买?\n"
                    "[Y/y] 是\t[N/n]否\n" % expense)
    while True:
        is_buy = input(">>> ")
        if is_buy == "Y" or is_buy == "y":  # 确定购买
            is_succeed = bank.pay_money(acc, expense)  # 支付, 得到支付操作结果
            if is_succeed:  # 支付成功
                print_log(INFO, "付款成功, 你的当前余额为: %s" % acc['balance'])
                return
            else:  # 支付失败
                print_log(WARNING, "余额不足无法购买")
                return
        elif is_buy == "N" or is_buy == "n":  # 不购买
            print_log(INFO, "已退出")
            return
        else:
            print_log(ERROR, "无效输入")


def shop_list_set(shopping_list):
    """
    合并购物车重复商品
    :param shopping_list: 购物车商品
    :return: 合并后的[商品, 购买数量]列表
    """
    set_list = set(shopping_list)
    record = []
    for name in set_list:
        record.extend([name, goods_dict[name], shopping_list.count(name)])
    return record


def print_log(level, msg):
    """
    高亮显示
    :param level: INFO->通知, WARNING->警告 ERROR->错误
    :param msg: 需高亮显示的字符串
    :return: None
    """
    if level == "INFO":
        format_msg = "\033[32;1m{}\033[0m"
    elif level == "WARNING":
        format_msg = "\033[31;1m{}\033[0m"
    else:  # level == "ERROR"
        format_msg = "\033[41;1m{}\033[0m"
    print(format_msg.format(msg))


def get_chinese_num(s):
    """
    统计字符串中汉字个数
    :param s: 要统计汉字个数的字符串
    :return: 汉字个数
    """
    num_of_chinese = 0
    for word in s:
        if not word.isdigit():
            num_of_chinese += 1
    return num_of_chinese


def formatted_output(s1, s2, s3):  # 清单格式化输出
    print(s1.center(15-get_chinese_num(s1)) + s2.center(15-get_chinese_num(s2)) + s3.center(15-get_chinese_num(s3)))


def print_list(list_type, printed_list):
    """
    格式化打印列表
    :param list_type: 'good'->商品列表 "shop list"->购物车列表
    :param printed_list: 要打印的列表
    :return: None
    """
    if list_type == "goods":
        print(" 商品列表 ".center(41, "-"))
        formatted_output("编号", "商品", "单价")
        for index, good in enumerate(printed_list):
            formatted_output(str(index), good["name"], str(good["price"]))
        print("".center(45, "-"))
        return
    else:  # list_type == "shop list"
        shop_list = printed_list
        print(" 购物车 ".center(41, "-"))
        if len(shop_list) == 0:
            print("未购买任何商品".center(38))
            return
        formatted_output("商品", "单价", "数量")
        for j in range(0, len(shop_list)-2, 3):
            formatted_output(shop_list[j], str(shop_list[j + 1]), str(shop_list[j + 2]))
        print("".center(45, "-"))


def shopping(acc):
    """
    进入购物车操作界面
    :param acc: 用户信息字典
    :return: None
    """
    expense = 0  # 购物车商品总金额
    shopping_list = []  # 购物车列表
    while True:  # 进行购物
        print_list("goods", goods)
        user_choice = input("选择要买的商品编号: ")
        if user_choice.isdigit():
            user_choice = int(user_choice)
        elif user_choice == 'q' or user_choice == 'Q':  # 退出
            shopping_list = shop_list_set(shopping_list)
            print_list("shop list", shopping_list)  # 打印购物车列表
            payment(acc, expense)
            return
        else:
            print_log(ERROR, "无效输入")
            continue
        if (user_choice >= 0) and (user_choice < len(goods)):  # 添加购物车
            add_item = goods[user_choice]
            shopping_list.append(add_item["name"])
            expense += add_item["price"]
            print_log(INFO, "已将 %s 加入购物车, 已加商品总计%d元" % (add_item["name"], expense))
        else:
            print_log(ERROR, "商品编号 [%d] 不存在!" % user_choice)
