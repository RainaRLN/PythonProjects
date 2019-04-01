#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5

from core.logger import *


class Teacher:

    def __init__(self, teacher_name, teacher_password, teacher_school_obj):
        self.teacher_name = teacher_name
        self.name = self.teacher_name
        self.password = teacher_password
        self.teacher_school = teacher_school_obj
        self.teacher_class = {}

    def teacher_bond_class(self, class_obj):
        self.teacher_class[class_obj.class_name] = class_obj

    def show_classroom(self):
        print("你当前管理的班级有:")
        for class_name in self.teacher_class:
            print("  " + class_name, end='\t')
        print()

    def show_student(self):
        self.show_classroom()
        class_name = input("你要查看哪个班级的学员?(请输入班级名)\n>>> ")
        if class_name in self.teacher_class:
            selected_classroom = self.teacher_class[class_name]
            selected_classroom.show_student()
            return selected_classroom
        else:
            print_log(ERROR, "请输入正确的班级名!")
                
    def change_grade(self):
        selected_classroom = self.show_student()
        if not selected_classroom:
            return None, None
        selected_student_name = input("请输入要修改成绩的学员名: ")
        if selected_student_name in selected_classroom.class_student:
            selected_student = selected_classroom.class_student[selected_student_name]
            print("%s 当前的成绩为 %s" % (selected_student_name, selected_student.grade))
            grade = input("请输入成绩: ")
            selected_student.grade = grade
            print_log(INFO, "修改成功!\n%s 当前的成绩为 %s" % (selected_student_name, selected_student.grade))
            return selected_classroom, selected_student
        else:
            print_log(ERROR, "请输入正确的学员名!")
            return None, None
