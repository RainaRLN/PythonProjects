#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/13


"""
    基础要求：
    1、启动程序后，输入用户名密码后，让用户输入工资，然后打印商品列表
    2、允许用户根据商品编号购买商品
    3、用户选择商品后，检测余额是否够，够就直接扣款，不够就提醒
    4、可随时退出，退出时，打印已购买商品和余额
    5、在用户使用过程中， 关键输出，如余额，商品已加入购物车等消息，需高亮显示

    扩展需求：
    1、用户下一次登录后，输入用户名密码，直接回到上次的状态，即上次消费的余额什么的还是那些，再次登录可继续购买
    2、允许查询之前的消费记录
"""

import time
import json

INFO = "INFO"
ERROR = "ERROR"
WARNING = "WARNING"
ALL = "ALL"
LATEST = "LATEST"


def get_time():  # 获取时间
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_chinese_len(s):
    len_of_chinese = 0
    for word in s:
        if not word.isdigit():
            len_of_chinese += 1
    return len_of_chinese


def print_log(level, msg):  # 高亮提示
    if level == "INFO":
        format_msg = "\033[32;1m{}\033[0m"
    elif level == "WARNING":
        format_msg = "\033[31;1m{}\033[0m"
    else:  # level == "ERROR"
        format_msg = "\033[41;1m{}\033[0m"
    print(format_msg.format(msg))


def formatted_output(s1, s2, s3):  # 清单格式化输出
    print(s1.center(15-get_chinese_len(s1)) + s2.center(15-get_chinese_len(s2)) + s3.center(15-get_chinese_len(s3)))


def save_shop_list(shopping_list):  # 保存购物记录
    set_list = set(shopping_list)
    record = []
    for name in set_list:
        record.extend([name, goods_dict[name], shopping_list.count(name)])
    record.append(get_time())
    user.append(record)


def save_records():  # 保存用户信息
    file = open("user_profile.json", "w")
    json.dump(info, file)
    file.close()


def top_up():  # 充值
    while True:
        money = input("请输入充值金额: ")
        if money.isdigit():
            user[2] += int(money)
            save_records()
            print_log(INFO, "你已成功充值%s元, 当前余额为%s元" % (money, user[2]))
            return
        else:
            print_log(ERROR, "请输入数字")


def is_top_up():  # 选择是否充值
    while True:
        decision = input("是否充值[Y/N]: ")
        if decision == 'Y' or decision == 'y':
            top_up()
            break
        elif decision == 'N' or decision == 'n':
            return 1
        else:
            print_log(ERROR, "无效输入")


def print_list(list_type, part=ALL):
    if list_type == "goods":
        print(" 商品列表 ".center(41, "-"))
        formatted_output("编号", "商品", "单价")
        for index, good in enumerate(goods):
            formatted_output(str(index), good["name"], str(good["price"]))
        return
    elif list_type == "shop list" and part == 'LATEST':
        shop_list = [user[-1]]
        print(" 已购商品 ".center(41, "-"))
    else:  # list_type == "shop_list" and part == 'ALL'
        shop_list = user[3:]
        print(" 历史记录 ".center(41, "-"))
    for i in shop_list:
        print('\n' + i[-1].center(45))  # 打印时间
        if len(i) == 1:
            print("未购买任何商品".center(38))
            continue
        formatted_output("商品", "单价", "数量")
        for j in range(0, len(i)-3, 3):
            formatted_output(i[j], str(i[j + 1]), str(i[j + 2]))
    print("".center(45, "-"))


def shopping():  # 购物
    while user[2] <= 0:  # 判断是否还有余额
        print_log(WARNING, "你的账户余额为0, 需要充值才可进行购物")
        if is_top_up():  # 未充值
            print_log(WARNING, "余额不足无法进行购物, 已返回上级菜单")
            return
    else:  # 购买商品
        balance = user[2]
        shopping_list = []
        while True:
            print_list("goods", ALL)
            user_choice = input("选择要买的商品编号: ")
            if user_choice.isdigit():
                user_choice = int(user_choice)
            elif user_choice == 'q' or user_choice == 'Q':
                user[2] = balance
                save_shop_list(shopping_list)
                save_records()
                print_list("shop list", LATEST)  # 打印本次购买记录
                print_log(INFO, "你的当前余额为: %s" % balance)
                return
            else:
                print_log(ERROR, "无效输入")
                continue
            if (user_choice >= 0) and (user_choice < len(goods)):
                add_item = goods[user_choice]
                if add_item["price"] <= balance:  # 判断余额是否足够
                    shopping_list.append(add_item["name"])
                    balance -= add_item["price"]
                    print_log(INFO, "已将 %s 加入购物车, 当前余额为 %s " % (add_item["name"], balance))
                else:  # 余额不足
                    print_log(WARNING, "你的余额只剩 %s 了, 无法购买" % balance)
            else:
                print_log(ERROR, "商品编号 [%d] 不存在!" % user_choice)


def end():  # 退出
    save_records()
    print_log(WARNING, "已退出!")
    exit()


def switch(case):  # 选择后续操作
    if case == '1':
        top_up()  # 充值
    elif case == '2':
        shopping()  # 购物
    elif case == '3':
        print_list("shop list", ALL)  # 查看历史购买记录
    elif case == 'q' or case == 'Q':
        end()  # 退出
    else:
        print("\033[41;1m无效输入\033[0m")

goods = [
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998}
]

goods_dict = {}
for item in goods:
    goods_dict[item["name"]] = item["price"]

f = open("user_profile.json", "r")
info = json.load(f)
f.close()

option = """
请选择下续操作:
    1 充值
    2 购物
    3 查看历史记录
    Q 退出
"""

while True:
    # 输入用户名密码登录
    username = input("username: ")
    password = input("password: ")

    # 验证用户名密码
    for user in info:
        if username == user[0] and password == user[1]:
            print("\033[31;1m登录成功!\033[0m")
            while True:  # 进入购物程序
                choice = input(option + ">>> ")
                switch(choice)
            break
    else:
        print("\033[41;1m用户名或密码错误,请重试\033[0m")
