#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/29

import json
user_dicts = [
    {
        'id': 'Tom',  # 用户名
        'password': '123',  # 密码
        'credit': 15000,  # 信用额度
        'balance': 3000,  # 余额
        'enroll_date': '2016-01-02',  # 注册日期
        'status': 3  # 1-3 = normal, 0,-1 = locked
    },
    {
        'id': 'Alex',
        'password': 'abc',
        'credit': 15000,
        'balance': 15000,
        'enroll_date': '2016-01-02',
        'status': 3
    }
]
admin_dicts = [
    {
        'id': 'admin1',
        'password': '123'
    },
    {
        'id': 'admin',
        'password': 'abc'
    }
]

print(json.dumps(user_dicts))
print(json.dumps(admin_dicts))
