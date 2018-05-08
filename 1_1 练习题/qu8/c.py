#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/2

"""
  使用while循环输出100-50,从大到小,如100,99,98, 到50时再从0循环输出到50然后结束
"""

n = 100

while n >= 0:
    if n >= 50:
        print('%d,' % n, end="")
    else:
        print('%d,' % (49 - n), end="")
    n -= 1
print(50)
