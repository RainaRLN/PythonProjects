#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/22

"""
 写一个简单的员工信息增删改查程序，需求如下：
    1.可进行模糊查询，语法至少支持下面3种查询语法:
        find name,age from staff_table where age > 22
        find * from staff_table where dept = "IT"
        find * from staff_table where enroll_date like "2013"
    2.可创建新员工纪录，以phone做唯一键(即不允许表里有手机号重复的情况)，staff_id需自增
        add staff_table Alex Li,25,134435344,IT,2015-10-29
    3.可删除指定员工信息纪录，输入员工id，即可删除
        del from staff_table where id=3
    4.可修改员工信息
        UPDATE staff_table SET dept="Market" where dept = "IT"
        UPDATE staff_table SET age=25 where name = "Alex Li"
    5.以上每条语名执行完毕后，要显示这条语句影响了多少条纪录。比如查询语句就显示查询出了多少条、修改语句就显示修改了多少条等
"""

INFO = "INFO"
ERROR = "ERROR"
ID, NAME, AGE, PHONE, DEPT, DATE = 0, 1, 2, 3, 4, 5
COLUMN = ['id', 'name', 'age', 'phone', 'dept', 'enroll_date', 'staff_table']
KEY_WORDS = ['find', 'add', 'del from', 'UPDATE', 'from', 'SET', 'where',
             '>', '<', '!=', '=', '>=', '<=', 'like']
staff_table = []
type_of_col = dict(zip(COLUMN[:-1], ['int', 'str', 'int', 'str', 'str', 'str', 'str']))
s2v = dict(zip(COLUMN, [ID, NAME, AGE, PHONE, DEPT, DATE, staff_table]))  # 字符串转变量名


def load_data():  # 将员工信息保存至列表
    with open("data.txt", 'r', encoding='utf-8') as data:
        for line in data:
            temp = line.strip().split(',')
            staff_table.append(temp)  # list类型员工信息


def save_changes():  # 保存更改的员工信息
    with open("data.txt", 'w', encoding='utf-8') as data:
        index = 1
        for staff in staff_table:
            staff[ID] = str(index)  # 若删除了员工信息,需重新编号
            data.write(','.join(staff) + '\n')
            index += 1


def print_log(level, msg):  # 高亮提示
    if level == "INFO":
        format_msg = "\033[32;1m{}\033[0m"
    else:  # level == "ERROR"
        format_msg = "\033[41;1m{}\033[0m"
    print(format_msg.format(msg))


def cmp(obj1, obj2, type_):
    """
    实现数字的比较,字符串的匹配
    :param obj1: 数据1
    :param obj2: 数据2
    :param type_: 数据类型
    :return: 比较结果: 大于->1, 小于->-1, 等于->0, like->2
    """
    if type_ == 'int':
        if obj1 == obj2:
            return 0
        elif int(obj1) > int(obj2):
            return 1
        elif int(obj1) < int(obj2):
            return -1
    else:
        if obj1 == obj2:
            return 0
        elif obj2 in obj1:
            return 2


def pick_out(obj1, obj2, opr):
    """
    筛选符合where条件的ID
    :param obj1: 数据1
    :param obj2: 数据2
    :param opr: 比较运算符
    :return: 符合条件的ID的列表
    """
    operators = {  # 满足条件的cmp返回值
        '>': [1],
        '<': [-1],
        '!=': [1, -1],
        '=': [0],
        '>=': [1, 0],
        '<=': [-1, 0],
        'like': [0, 2]
    }
    picked_id = []
    for staff in staff_table:
        result = cmp(staff[s2v[obj1]], obj2.strip('"'), type_of_col[obj1])  # 比较两操作数
        if result in operators[opr]:  # 筛选符合where条件的ID
            picked_id.append(staff[ID])
    return picked_id


def is_find(keywords, tokens):
    """
    执行find操作
    :param keywords: 指令列表
    :param tokens: 指令与操作对象的字典
    :return: None
    """
    tokens['find'] = tokens['find'].split(',')  # 需要查找的列
    table = s2v[tokens['from'].strip()]  # 需要对其进行操作的表
    if 'where' in keywords:  # 如果有限制条件
        picked_id = pick_out(tokens['where'], tokens[keywords[-1]], keywords[-1])  # 筛选符合条件的ID
    else:  # 无限制条件, 查找所有ID
        picked_id = [str(i+1) for i in range(len(table))]
    print_log(INFO, "已查出%d条记录" % len(picked_id))
    for staff in table:  # 输出查找结果
        if staff[ID] in picked_id:
            if tokens['find'][0] == '*':  # 输出所有列
                print(','.join(staff))
            else:  # 输出需要的列
                for col in tokens['find']:
                    print(staff[s2v[col]], end=' ')
                print()  # 换行


def is_add(tokens):
    """
    执行add操作
    :param tokens: {'add': add后的字符串]
    :return: None
    """
    tokens['add'] = tokens['add'].split(' ', 1)  # tokens['add'] = ['对其进行操作的表', '添加的信息']
    table = s2v[tokens['add'][0].strip()]
    new_id = str(len(table) + 1)  # staff_id自增
    new_staff = [new_id]
    new_staff.extend(tokens['add'][-1].split(','))
    for staff in table:
        if new_staff[PHONE] == staff[PHONE]:
            print_log(ERROR, '该员工的信息已存在')
            break
    else:
        table.append(new_staff)
        save_changes()
        print_log(INFO, '已添加一条员工信息')
        print(','.join(new_staff))


def is_del(keywords, tokens):
    """
    执行del操作
    :param keywords: 指令列表
    :param tokens: 指令与操作对象的字典
    :return: None
    """
    table = s2v[tokens['del from'].strip()]  # 对其进行操作的表格
    picked_id = pick_out(tokens['where'], tokens[keywords[-1]], keywords[-1])  # 筛选符合条件的ID
    print_log(INFO, "已删除%d条记录" % len(picked_id))
    # for staff in table:  # 一边遍历一边删会出错
    #     if staff[ID] in picked_id:
    #         table.remove(staff)
    table_old = table[:]
    for staff in table_old:
        if staff[ID] in picked_id:
            print(','.join(staff))
            table.remove(staff)  # 删除符合条件的信息
    save_changes()


def is_update(keywords, tokens):
    """
    执行update操作
    :param keywords:指令列表
    :param tokens: 指令与操作对象的字典
    :return: None
    """
    table = s2v[tokens['UPDATE'].strip()]  # 对其进行操作的表格
    tokens['SET'] = tokens['SET'].split(' ')  # tokens['SET'] = ['更改的列', '更改后的值']
    if 'where' in keywords:  # 若有限制条件
        picked_id = pick_out(tokens['where'], tokens[keywords[-1]], keywords[-1])
    else:
        picked_id = [str(i + 1) for i in range(len(table))]
    print_log(INFO, "已更新%d条记录" % len(picked_id))
    for staff in table:
        if staff[ID] in picked_id:  # 更改信息
            staff[s2v[tokens['SET'][0].strip('"')]] = tokens['SET'][-1].strip('"')
            print(staff)
    save_changes()


def tokenizer(cmd):
    """
    提取指令和操作对象
    :param cmd: 命令字符串
    :return: 指令列表, 指令与操作对象的字典
    """
    keywords = []
    tokens = {}
    for i in KEY_WORDS:
        if i in cmd:
            keywords.append(i)
            cmd = ';'.join(cmd.split(i))
            if i == 'SET':
                cmd = ' '.join(cmd.split('=', 1))
    cmd = cmd.strip().split(";")
    for key in keywords:
        tokens[key] = cmd[keywords.index(key) + 1].strip()
    return keywords, tokens


def parser(cmd):
    """
    解释命令字符串
    :param cmd: 命令字符串
    :return: None
    """
    keywords, tokens = tokenizer(cmd)  # 提取指令和操作对象
    if keywords[0] == 'find':  # 执行find操作
        is_find(keywords, tokens)
    elif keywords[0] == 'add':  # 执行add操作
        is_add(tokens)
    elif keywords[0] == 'del from':  # 执行del操作
        is_del(keywords, tokens)
    elif keywords[0] == 'UPDATE':  # 执行UPDATE操作
        is_update(keywords, tokens)
    else:
        print_log(ERROR, '语法错误')


load_data()
while True:
    command = input(">>> ")
    if command == 'exit':  # 命令为'exit', 退出
        exit()
    else:
        parser(command)
