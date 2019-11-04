#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import logging


def sklog_init(log_name):
    from conf.skplugins_conf import log_path
    sklog = logging.getLogger()  # 不加名称设置root logger
    sklog.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S.%03d')

    # 使用FileHandler输出到文件
    log_file = log_path+log_name
    fhlog = logging.FileHandler(log_file)
    fhlog.setLevel(logging.INFO)
    fhlog.setFormatter(formatter)

    # 使用StreamHandler输出到屏幕
    chlog = logging.StreamHandler()
    chlog.setLevel(logging.INFO)
    chlog.setFormatter(formatter)

    # 添加两个Handler
    sklog.addHandler(chlog)
    sklog.addHandler(fhlog)
    return sklog

if __name__ == "__main__":
    pass
    # sklog.info('this is info message')
    # sklog.warn('this is warn message')