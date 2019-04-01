#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5

from conf.setting import *
import sys
from core.logger import *


class Interface:

    def __init__(self):
        self.user_dict = {}
        self.user = None
        self.menu = ""

    def login(self):
        while True:
            username = input("username: ")
            password = input("password: ")
            for key in self.user_dict:
                if self.user_dict[key].name == username and self.user_dict[key].password == password:
                    print_log(INFO, "登录成功")
                    log("login").info(username + "登录成功")
                    return self.user_dict[key]
            print_log(ERROR, "用户名或密码错误, 请重新输入")
            log("Log in").error("登录失败, 用户名或密码错误")

    def run(self, obj):
        self.user = obj
        while True:
            print(self.menu)
            user_choice = input("请输入命令: ").strip()
            if hasattr(self, user_choice):
                getattr(self, user_choice)()
            else:
                print_log(ERROR, "输入的命令有误, 请重新输入!")
                log("cmd error").error("输入的命令有误")

    @staticmethod
    def exit():
        log("exit").info("退出程序")
        sys.exit("已退出")


class ManagerInterface(Interface):

    def __init__(self):
        super().__init__()
        self.user_dict = INFO_DICT['school']
        self.menu = """
******** 管理员视图 ********
创建课程: create_course
创建班级: create_classroom
创建学生: create_student
创建讲师: create_teacher
退出程序: exit
***************************
        """

    def create_course(self):
        self.user.show_course()
        course_name = input("请输入课程名: ").strip()
        course_price = input("请输入课程价格: ").strip()
        course_period = input("请输入课程周期: ").strip()
        if course_name in self.user.school_course:
            print_log(WARNING, "课程已存在, 课程信息更新完成")
            log("create course").warning(course_name + "课程信息更新")
        else:
            print_log(INFO, "课程添加成功")
            log("create course").info(course_name + "课程添加成功")
        course_obj = self.user.create_course(course_name, course_price, course_period)
        save_db('course', {course_name: course_obj})
        save_db('school', {self.user.school_name: self.user})

    def create_classroom(self):
        self.user.show_classroom()
        class_name = input("输入要创建的班级名: ").strip()
        self.user.show_course()
        course_name = input("请输入关联的课程名: ").strip()
        if class_name not in self.user.school_class:
            if course_name in self.user.school_course:
                class_course_obj = self.user.school_course[course_name]
                classroom_obj = self.user.create_classroom(class_name, class_course_obj)
                save_db('classroom', {class_name: classroom_obj})
                save_db('school', {self.user.school_name: self.user})
                print_log(INFO, "班级创建成功")
                log("create classroom").info(class_name + "班级添加成功")
            else:
                print_log(ERROR, "关联的课程不存在")
                log("create classroom").error(class_name + "关联的课程不存在")
        else:
            print_log(WARNING, "班级已经存在")
            log("create classroom").warning(class_name + "班级已存在")

    def create_student(self):
        self.user.show_student()
        student_name = input("请输入要添加的学员名: ").strip()
        student_password = input("请输入学员密码: ").strip()
        if student_name not in self.user.school_student:
            print_log(INFO, "成功添加学员")
            log("create student").info(student_name + "学员添加成功")
        else:
            print_log(WARNING, "学员已经存在，学员信息更新完成")
            log("create student").warning(student_name + "学员信息更新")
        student_obj = self.user.create_student(student_name, student_password)
        save_db('school', {self.user.school_name: self.user})
        save_db('student', {student_name: student_obj})

    def create_teacher(self):
        self.user.show_teacher()
        teacher_name = input("请输入要添加的讲师名: ").strip()
        teacher_password = input("请输入讲师密码: ").strip()
        if teacher_name not in self.user.school_teacher:
            print_log(INFO, "成功添加讲师")
            log("create teacher").info(teacher_name + "讲师添加成功")
        else:
            print_log(WARNING, "讲师已经存在，讲师信息更新完成")
            log("create student").warning(teacher_name + "讲师信息更新")
        teacher_obj = self.user.create_teacher(teacher_name, teacher_password)
        save_db('school', {self.user.school_name: self.user})
        save_db('teacher', {teacher_name: teacher_obj})


class TeacherInterface(Interface):

    def __init__(self):
        super().__init__()
        self.user_dict = INFO_DICT['teacher']
        self.menu = """
********** 讲师视图 **********
绑定班级: teacher_bond_class
查看学员: show_student
修改成绩: change_student_grade
退出程序: exit
*****************************
        """

    def show_student(self):
        self.user.show_student()

    def change_student_grade(self):
        selected_classroom, selected_student = self.user.change_grade()
        if selected_student and selected_classroom:
            log("change grade").info(selected_student.student_name + "成绩修改成功")
            save_db('student', {selected_student.student_name: selected_student})
            save_db('classroom', {selected_classroom.class_name: selected_classroom})
            save_db('teacher', {self.user.teacher_name: self.user})
            save_db('school', {self.user.teacher_school.name: self.user.teacher_school})

    def teacher_bond_class(self):
        self.user.teacher_school.show_classroom()
        self.user.show_classroom()
        class_name = input("请输入要关联的班级名: ").strip()
        if class_name in self.user.teacher_class:
            print_log(WARNING, "你已关联该班级!")
            log("teacher bond classroom").warning(self.user.teacher_name + "讲师已关联班级" + class_name)
            return
        elif class_name in self.user.teacher_school.school_class:
            class_obj = self.user.teacher_school.school_class[class_name]
            self.user.teacher_bond_class(class_obj)
            save_db('teacher', {self.user.teacher_name: self.user})
            save_db('classroom', {class_obj.class_name: class_obj})
            save_db('school', {self.user.teacher_school.name: self.user.teacher_school})
            print_log(INFO, "班级关联成功")
            log("teacher bond classroom").info(self.user.teacher_name + "讲师关联班级" + class_name + "成功")
        else:
            print_log(ERROR, "关联的班级不存在")
            log("teacher bond classroom").error(self.user.teacher_name + "讲师关联的班级不存在")


class StudentInterface(Interface):

    def __init__(self):
        super().__init__()
        self.user_dict = INFO_DICT['student']
        self.menu = """
******** 学员视图 ********
交学费: pay_tuition
关联班级: student_bond_class
查看成绩: show_grade
退出程序: exit
***************************
        """

    def pay_tuition(self):
        if self.user.pay_tuition():
            log("pay tuition").info(self.user.student_name + "学费支付成功")
            save_db('student', {self.user.student_name: self.user})
            save_db('school', {self.user.student_school.name: self.user.student_school})

    def student_bond_class(self):
        self.user.student_school.show_classroom()
        class_name = input("请输入要关联的班级名: ").strip()
        if class_name in self.user.student_school.school_class:
            class_obj = self.user.student_school.school_class[class_name]
            if class_obj == self.user.student_class:
                print_log(WARNING, "你已关联该班级!")
                log("student bond classroom").warning(self.user.student_name + "学员已关联班级" + class_name)
            else:
                self.user.student_bond_class(class_obj)
                save_db('student', {self.user.student_name: self.user})
                save_db('classroom', {class_obj.class_name: class_obj})
                save_db('school', {self.user.student_school.name: self.user.student_school})
                print_log(INFO, "班级关联成功")
                log("student bond classroom").info(self.user.student_name + "学员关联班级" + class_name + "成功")
        else:
            print_log(ERROR, "关联的班级不存在")
            log("student bond classroom").error(self.user.student_name + "学员关联的班级不存在")

    def show_grade(self):
        self.user.show_grade()


def save_db(info_type, info):
    INFO_DICT[info_type].update(info)
    with open(INFO_PATH, 'wb') as db:
        pickle.dump(INFO_DICT, db)
