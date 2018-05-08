#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/2

"""
  假设一年期定息利率为3.25%,计算一下需要过多少年,一万元的一年定期存款连本带息能翻番
"""

s = money = 10000
interest_rates = 0.0325
year = 0
while s < 2*money:
    year += 1
    s = s * (1 + interest_rates)
print("需要存%d年,一万元的一年定期存款连本带息能翻番,共%.2f元" % (year, s))
