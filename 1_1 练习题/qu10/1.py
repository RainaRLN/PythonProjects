#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/2

"""
  需求: 等待用户输入姓名、地点、爱好, 根据用户的名字和爱好进行任意显示
  如: 敬爱可爱的xxx, 最喜欢在xxx地方干xxx
"""

name = input("name: ")
place = input("place: ")
hobby = input("hobby: ")

print("敬爱可爱的%s,最喜欢在%s地方干%s" % (name, place, hobby))
