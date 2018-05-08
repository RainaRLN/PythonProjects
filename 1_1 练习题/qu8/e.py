#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/2

"""
  使用while循环实现输出1-100内的所有偶数
"""

n = 1

while n <= 100:
    if n % 2 == 0:
        print(n)
    n += 1
