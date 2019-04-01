#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/7/3

import logging
from conf.setting import LOG_PATH

INFO = "INFO"
ERROR = "ERROR"
WARNING = "WARNING"


def log(log_type):

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logger = logging.getLogger(log_type)
    logger.setLevel("INFO")

    handler = logging.FileHandler(filename=LOG_PATH, encoding="utf-8")
    handler.setLevel("INFO")
    handler.setFormatter(logging.Formatter(log_format))

    logger.addHandler(handler)

    return logger


def print_log(level, msg):  # 高亮提示
    if level == "INFO":
        format_msg = "\033[32;1m{}\033[0m"
    elif level == "WARNING":
        format_msg = "\033[31;1m{}\033[0m"
    else:  # level == "ERROR"
        format_msg = "\033[41;1m{}\033[0m"
    print(format_msg.format(msg))
