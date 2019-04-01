#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5

from core.logger import *


class Student:

    def __init__(self, student_name, student_password, student_school_obj):
        self.student_name = student_name
        self.name = self.student_name
        self.password = student_password
        self.student_school = student_school_obj
        self.grade = 0  # 学生成绩
        self.is_paid = False  # 是否交学费
        self.student_class = None

    def pay_tuition(self):
        if not self.student_class:
            print_log(ERROR, "未绑定班级")
            return
        if self.is_paid:
            print_log(WARNING, "学费已交")
            return
        else:
            while True:
                choice = input("需支付{}元, 是否支付Y/N?\n>>> ".format(self.student_class.class_course.course_price))
                if choice == 'Y' or choice == "y":
                    self.is_paid = True
                    print_log(INFO, "支付成功")
                    return True
                elif choice == 'N' or choice == "n":
                    print_log(WARNING, "已取消支付")
                    return
                else:
                    print_log(ERROR, "输入无效")

    def student_bond_class(self, student_class_obj):
        self.student_class = student_class_obj
        student_class_obj.class_student[self.student_name] = self

    def show_grade(self):
        if not self.student_class:
            print_log(ERROR, "未绑定班级")
            return
        print_log(INFO, "%s 你的 %s 的成绩为 %s"
                  % (self.student_name, self.student_class.class_course.course_name, self.grade))
