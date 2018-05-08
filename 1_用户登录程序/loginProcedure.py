#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/3

"""
    基础需求：
        让用户输入用户名密码
        认证成功后显示欢迎信息
        输错三次后退出程序

    升级需求：
        可以支持多个用户登录 (提示，通过列表存多个账户信息)
        用户3次认证失败后，退出程序，再次启动程序尝试登录时，还是锁定状态（提示:需把用户锁定的状态存到文件里）
"""

import time
import json


def end():
    file = open("userList.json", "w")
    json.dump(info, file)
    file.close()
    exit()


def choose():
    print("退出[1] 或者 重新登录[2]")
    while True:
        is_exit = input()
        if is_exit == '1':
            end()
        elif is_exit == '2':
            break
        else:
            print("无效字符, 请输入 1 或 2")
            continue

f = open("userList.json", "r")
info = json.load(f)
f.close()

while True:
    u = False  # 此用户不存在
    # 输入用户名密码
    username = input("username: ")
    password = input("password: ")

    # 验证用户名与密码
    for i in info:
        if username == i[0]:
            u = True  # 用户存在
            if i[2] <= 0:  # 没有登录机会
                t = time.time() - i[3]
                if t >= 30:
                    i[2] = 3
                else:
                    print("尝试登录次数过多,请%ds后重试" % (30 - t))
                    end()

            # 还有登录机会
            if password == i[1]:
                print("登录成功")
                i[2] = 3
                end()  # 登录成功,退出
            else:
                i[2] -= 1  # 密码错误,剩余次数-1
                if i[2] > 0:
                    print("用户名或密码错误, 你还可尝试%d次机会" % i[2])
                else:
                    print("尝试登录次数过多,请30s后重试")
                    i[3] = time.time()
                    end()

    # 查找不到此用户
    if not u:
        print("无此用户, 是否创建新用户? [Y/N]")
        while True:
            is_create = input()
            if is_create == 'Y' or is_create == 'y':
                # 添加新用户
                print("请输入你要创建的用户名及密码:")
                while True:  # 创建用户
                    uu = False
                    newU = input("username: ")
                    newP = input("password: ")
                    for j in info:
                        if newU == j[0]:
                            print("此用户名已存在,请重新输入")
                            uu = True  # 用户已存在
                            break
                    if not uu:  # 此用户名尚未注册
                        break

                new_info = [newU, newP, 3, 0]
                info.append(new_info)
                print("创建成功!")
                choose()  # 退出或重新登录
                break
            elif is_create == 'N' or is_create == 'n':
                choose()  # 退出或重新登录
                break
            else:
                print("无效字符, 请输入 Y 或 N")
                continue
