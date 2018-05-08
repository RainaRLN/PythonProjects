#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/2

"""
  实现用户输入用户名和密码，当用户名为seven且密码为123时，显示登录成功，否则登录失败
"""

USERNAME = 'seven'
PASSWORD = '123'

username = input("username: ")
password = input("password: ")

if username == USERNAME and password == PASSWORD:
    print("登录成功！")
else:
    print("登录失败！")
