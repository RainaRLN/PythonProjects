#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5

from cls.course import Course
from cls.classroom import Classroom
from cls.teacher import *
from cls.student import Student


class School:
    """
    学校类, 包含学校名, 课程, 教室, 讲师
    通过学校创建课程, 教室
    """

    def __init__(self, school_name, manager_name, manager_password):
        self.school_name = school_name
        self.name = manager_name
        self.password = manager_password
        self.school_course = {}
        self.school_class = {}
        self.school_teacher = []
        self.school_student = []

    def create_course(self, course_name, course_price, course_period):
        course_obj = Course(course_name, course_price, course_period)
        self.school_course[course_name] = course_obj
        return course_obj

    def create_classroom(self, class_name, class_course_obj):
        classroom_obj = Classroom(class_name, class_course_obj)
        self.school_class[class_name] = classroom_obj
        return classroom_obj

    def create_teacher(self, teacher_name, teacher_password):
        teacher_obj = Teacher(teacher_name, teacher_password, self)
        self.school_teacher.append(teacher_obj.teacher_name)
        return teacher_obj

    def create_student(self, student_name, student_password):
        student_obj = Student(student_name, student_password, self)
        self.school_student.append(student_obj.student_name)
        return student_obj

    def show_classroom(self, ):
        print("该学校的班级有:")
        for key in self.school_class:
            class_obj = self.school_class[key]
            course_obj = class_obj.class_course
            print("  班级名: %s\t课程: %s" % (class_obj.class_name, course_obj.course_name))

    def show_teacher(self):
        print("该学校的讲师有:")
        for teacher_name in self.school_teacher:
            print(teacher_name, end='\t')
        print()

    def show_course(self):
        print("该学校的课程有:")
        for key in self.school_course:
            course_obj = self.school_course[key]
            print("  课程名: %s\t价格: %s\t周期: %s\t"
                  % (course_obj.course_name, course_obj.course_price, course_obj.course_period))

    def show_student(self):
        print("该学校的学生有:")
        for student_name in self.school_student:
            print(student_name, end='\t')
        print()
