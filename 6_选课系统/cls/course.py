#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5


class Course:

    def __init__(self, course_name, course_price, course_period):
        self.course_name = course_name
        self.course_price = course_price
        self.course_period = course_period


    def __str__(self):
        return "课程名称：%s 价格" % self.course_name
