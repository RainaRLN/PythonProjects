#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/4/6

"""
    三级菜单 需求：
    可依次选择进入各子菜单
    可从任意一层往回退到上一层
    可从任意一层退出程序
    所需新知识点：列表、字典
"""

menu = {
    '北京': {
        '海淀': {
            '五道口': {
                'soho': {},
                '网易': {},
                'google': {}
            },
            '中关村': {
                '爱奇艺': {},
                '汽车之家': {},
                'youku': {},
            },
            '上地': {
                '百度': {},
            },
        },
        '昌平': {
            '沙河': {
                '老男孩': {},
                '北航': {},
            },
            '天通苑': {},
            '回龙观': {},
        },
        '朝阳': {},
        '东城': {},
    },
    '上海': {
        '闵行': {
            "人民广场": {
                '炸鸡店': {}
            }
        },
        '闸北': {
            '火车战': {
                '携程': {}
            }
        },
        '浦东': {},
    },
    '山东': {},
}

# # 很low的写法, 有错
# while True:
#     for i in menu:  # 打印一级菜单
#         print(i)
#     choice = input("选择进入1>>> ")
#     if choice in menu:
#         while True:
#             for i2 in menu[choice]:
#                 print(i2)
#             choice2 = input("选择进入2>>> ")
#             if choice2 in menu[choice]:
#                 while True:
#                     for i3 in menu[choice][choice2]:
#                         print(i3)
#                     choice3 = input("选择进入3>>> ")
#                     if choice3 in menu[choice][choice2]:
#                         while True:
#                             for i4 in menu[choice][choice2][choice3]:
#                                     print(i4)
#                             choice4 = input("输入b返回上一级>>>")  # TODO 应该每级都判断是不是空
#                             if choice4 == "b":
#                                 pass
#                             elif choice4 == "q":
#                                 print("已退出")
#                                 exit()
#                             else:
#                                 print("无效输入!")
#                     elif choice3 == "b":
#                         break
#                     elif choice3 == "q":
#                         print("已退出")
#                         exit()
#                     else:
#                         print("无效输入!")
#             elif choice2 == "b":
#                 break
#             elif choice2 == "q":
#                 print("已退出")
#                 exit()
#             else:
#                 print("无效输入!")
#     elif choice == "b" or choice == "q":
#         print("已退出")
#         exit()
#     else:
#         print("无效输入!")


# # 第二版
# menu_copy = [menu]
# level = 0
# while level >= 0:
#     for i in menu_copy[level]:
#         print(i)
#     if not menu_copy[level]:
#         print("已无选项,输入b返回上一级")
#     choice = input(">>> ")
#     if choice in menu_copy[level]:
#         menu_copy.append(menu_copy[level][choice])
#         level += 1
#     elif choice == 'b':
#         menu_copy.pop()
#         level -= 1
#     elif choice == 'q':
#         print("已退出")
#         exit()
#     else:
#         print("无效输入!")
# else:
#     print("已无上级菜单,已退出")


# # 第三版
# menu_copy = [menu]
# while menu_copy:
#     for i in menu_copy[-1]:
#         print(i)
#     if not menu_copy[-1]:
#         print("已无选项,输入b返回上一级")
#     choice = input(">>> ")
#     if choice in menu_copy[-1]:
#         menu_copy.append(menu_copy[-1][choice])
#     elif choice == 'b':
#         menu_copy.pop()
#     elif choice == 'q':
#         print("已退出")
#         exit()
#     else:
#         print("无效输入!")
# else:
#     print("已无上级菜单,已退出")


# 第四版
menu_copy = [menu]
choice = ''
while menu_copy and choice != 'q':
    for i in menu_copy[-1]:
        print(i)
    if not menu_copy[-1]:
        print("\033[1;35m已无选项,输入b返回上一级\033[0m")
    choice = input(">>> ")
    if choice in menu_copy[-1]:
        menu_copy.append(menu_copy[-1][choice])
    elif choice == 'b':
        menu_copy.pop()
    elif choice != 'q':
        print("\033[1;35m无效输入\033[0m")
else:
    print("\033[1;31m已退出\033[0m")
