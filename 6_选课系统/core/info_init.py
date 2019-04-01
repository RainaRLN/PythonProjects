#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/6/5

from cls.school import School
import os
import sys
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 数据信息路径
INFO_PATH = os.path.abspath(os.path.join(BASE_DIR, "db", "info.pk"))


if __name__ == '__main__':
    school1 = School('北京', 'admin1', '123')
    school2 = School('上海', 'admin2', 'abc')

    init_dict = {
        'school': {
            '北京': school1,
            '上海': school2,
        },
        'course': {

        },
        'classroom': {

        },
        'teacher': {

        },
        'student': {

        }
    }

    with open(INFO_PATH, 'wb') as f:
        pickle.dump(init_dict, f)

