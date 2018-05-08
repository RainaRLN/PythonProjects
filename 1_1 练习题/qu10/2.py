#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/2

"""
  输入一年份,判断该年份是否是闰年
  闰年: 能被4整除但不能被100整除,或能被400整除
"""

year = int(input("Please input a particular year: "))

if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
    print("%d年是闰年" % year)
else:
    print("%d年不是闰年" % year)

