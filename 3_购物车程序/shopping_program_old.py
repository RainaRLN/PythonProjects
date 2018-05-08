#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/10

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

import json


def save_records():  # 保存信息
    file = open("user_profile.json", "w")
    json.dump(info, file)
    file.close()


def top_up():  # 充值
    money = input("请输入充值金额: ")
    if money.isdigit():
        i[2] += int(money)
        save_records()
        print("你已成功充值\033[31;1m%s\033[0m元, 当前余额为\033[31;1m%s\033[0m元" % (money, i[2]))
    else:
        print("\033[41;1m请输入数字\033[0m")


def is_top_up():  # 选择是否充值
    while True:
        decision = input("是否充值[Y/N]: ")
        if decision == 'Y' or decision == 'y':
            top_up()
            break
        elif decision == 'N' or decision == 'n':
            return 1
        else:
            print("\033[41;1m无效输入\033[0m")


def shopping():  # 购物
    while i[2] <= 0:  # 判断是否还有余额
        print("\033[34;1m你的账户余额为0, 需要充值才可进行购物\033[0m")
        if is_top_up():  # 未充值
            print("\033[31;1m余额不足无法进行购物, 已返回上级菜单\033[0m")
            return
    else:  # 购买商品
        balance = i[2]
        shopping_list = []
        while True:
            for index, item in enumerate(goods):  # 打印商品列表
                print(index, item)
            user_choice = input("选择要买的商品编号: ")
            if user_choice.isdigit():
                user_choice = int(user_choice)
                if (user_choice >= 0) and (user_choice < len(goods)):
                    add_item = goods[user_choice]
                    if add_item["price"] <= balance:  # 判断余额是否足够
                        shopping_list.append(add_item)
                        balance -= add_item["price"]
                        print("已将 \033[34;1m%s\033[0m 加入购物车\n"
                              "当前余额为 \033[31;1m%s\033[0m" % (add_item["name"], balance))
                    else:  # 余额不足
                        print("\033[41;1m你的余额只剩 %s 了, 无法购买\033[0m" % balance)
                else:
                    print("\033[41;1m商品编号 [%d] 不存在!\033[0m" % user_choice)
            elif user_choice == 'q' or user_choice == 'Q':
                i[2] = balance
                i.append(shopping_list)
                save_records()
                view_history(i[-1])  # 查看本次购买记录
                print("\033[32;1m你的当前余额为: %s\033[0m" % balance)
                break
            else:
                print("\033[41;1m无效输入\033[0m")


def view_history(shop_list):  # 查看购物记录
    if shop_list:
        print("已购买商品".center(50, "-"))
        print("\033[34;1m")
        for item in shop_list:
            if not item:
                print(str("此次未购买").center(45, " "))
            else:
                print(str(item).center(45, " "))
        print("\033[0m")
        print("".center(50, "-"))
    else:
        print("\033[32;1m你未购买任何商品\033[0m")


def end():  # 退出
    save_records()
    print("\033[31;1m已退出!\033[0m")
    exit()


def switch(case):  # 选择后续操作
    if case == '1':
        top_up()  # 充值
    elif case == '2':
        shopping()  # 购物
    elif case == '3':
        view_history(i[3:])  # 查看历史购买记录
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

f = open("user_profile.json", "r")
info = json.load(f)
f.close()

msg = """
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
    for i in info:
        if username == i[0] and password == i[1]:
            print("\033[31;1m登录成功!\033[0m")
            while True:  # 进入购物程序
                choice = input(msg + ">>> ")
                switch(choice)
            break
    else:
        print("\033[41;1m用户名或密码错误,请重试\033[0m")
