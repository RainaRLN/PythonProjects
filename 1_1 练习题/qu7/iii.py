#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/2

"""
  实现用户输入用户名和密码，当用户名为seven或alex且密码为123时，显示登录成功，否则登录失败，失败时允许重复输入三次
"""

USERNAME1 = 'seven'
USERNAME2 = 'alex'
PASSWORD = '123'
count = 3

while count > 0:
    username = input("username: ")
    password = input("password: ")
    if (username == USERNAME1 or username == USERNAME2) and password == PASSWORD:
        print("登录成功！")
        break
    else:
        print("登录失败！")
    count -= 1
