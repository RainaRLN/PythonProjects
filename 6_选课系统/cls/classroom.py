#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5


class Classroom:

    def __init__(self, class_name, class_course_obj):
        self.class_name = class_name
        self.class_course = class_course_obj
        self.class_student = {}

    def show_student(self):
        print("此班级的学员有:")
        for student_name in self.class_student:
            print(student_name, end='\t')
        print()
