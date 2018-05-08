#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/5/1

"""
日志记录
"""

import logging
from conf.settings import LOG_PATH


def log(log_type):

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format=log_format)
    logger = logging.getLogger(log_type)
    return logger
