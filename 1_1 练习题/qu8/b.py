#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/2

"""
  使用while循环实现输出1,2,3,4,5,7,8,9,11,12
"""

n = 1

while n <= 12:
    if n != 6 and n != 10:
        if n != 12:
            print(str(n) + ',', end="")
        else:
            print(n)
    n += 1
