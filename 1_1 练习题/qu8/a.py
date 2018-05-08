#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/2

"""
  使用while循环实现输出2-3+4-5+6...+100的和
"""

n = 2
s = 0

while n <= 100:
    s = s + n*(-1)**(n % 2)
    n += 1

print("2-3+4-5+6...+100 =", s)
