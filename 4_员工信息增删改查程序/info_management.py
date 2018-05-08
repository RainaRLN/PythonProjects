#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/20

# from tabulate import tabulate

INFO = "INFO"
ERROR = "ERROR"
ID, NAME, AGE, PHONE, DEPT, DATE = 0, 1, 2, 3, 4, 5
COLUMN = ['id', 'name', 'age', 'phone', 'dept', 'enroll_date', 'staff_table']
KEY_WORDS = ['find', 'add', 'del from', 'UPDATE', 'from', 'SET', 'where',
             '>', '<', '!=', '=', '>=', '<=', 'like']
staff_table = dict([(k, []) for k in COLUMN[:-1]])  # 不能用dict.fromkeys(COLUMN,[]), value会指向同一列表

# 字符串转变量名
s2v = dict(zip(COLUMN, [ID, NAME, AGE, PHONE, DEPT, DATE, staff_table]))


def load_data():
    with open("data.txt", 'r', encoding='utf-8') as data:
        for line in data:
            temp = line.strip().split(',')
            for key in staff_table:
                value = temp[s2v[key]].strip()
                staff_table[key].append(value)


def save_changes():
    with open("data2.txt", 'w', encoding='utf-8') as data:
        for staff_id in staff_table['id']:
            line_temp = []
            for item in COLUMN[:-1]:
                line_temp.append(staff_table[item][int(staff_id)-1])
            data.write(','.join(line_temp) + '\n')


def print_log(level, msg):  # 高亮提示
    if level == "INFO":
        format_msg = "\033[32;1m{}\033[0m"
    else:  # level == "ERROR"
        format_msg = "\033[41;1m{}\033[0m"
    print(format_msg.format(msg))


# 提取指令和对象
def tokenizer(cmd):
    keywords = []
    tokens = {}
    for i in KEY_WORDS:
        if i in cmd:
            keywords.append(i)
            cmd = ';'.join(cmd.split(i))
    cmd = cmd.strip().split(";")
    for key in keywords:
        tokens[key] = cmd[keywords.index(key)+1].strip()
    return keywords, tokens


def parser(cmd):
    keywords, tokens = tokenizer(cmd)
    print(tokens)
    if keywords[0] == 'find':
        tokens['find'] = tokens['find'].split(',')
        print(tokens['find'])
        for index in staff_table['id']:
            for item in tokens['find']:
                print(s2v[tokens['from'].strip()][item.strip()][int(index)-1])
    elif keywords[0] == 'add':
        tokens['add'] = tokens['add'].split(' ', 1)
        new_id = int(staff_table['id'][-1]) + 1
        new_staff = [str(new_id)]
        new_staff.extend(tokens['add'][-1].split(','))
        print(new_staff)
        if new_staff[PHONE] in staff_table['phone']:
            print_log(ERROR, '该员工的信息已存在')
        else:
            for key in staff_table:
                value = new_staff[s2v[key]].strip()
                staff_table[key].append(value)
            print(staff_table)
            save_changes()
            print_log(INFO, '已添加一条员工信息')
    elif keywords[0] == 'del from':
        pass


load_data()
while True:
    command = input(">>> ")
    parser(command)
