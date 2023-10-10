# coding: utf8
""" 
@File: main.py
@Editor: PyCharm
@Author: Austin (From Chengdu.China) https://fairy.host
@HomePage: https://github.com/AustinFairyland
@OperatingSystem: Windows 11 Professional Workstation 23H2 Canary Channel
@CreatedTime: 2023-09-29
"""

import sys
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')

import time
from random import randint

from modules.journals import JournalsModule
from core import OperationClass

if __name__ == '__main__':
    while True:
        start_run_time = time.time()
        wait_time = randint(1, 10)
        git_operation = OperationClass(url_protocol='http')
        git_operation.commit('add')
        git_operation.push()
        JournalsModule.info('运行时长：{}秒'.format(time.time() - start_run_time))
        JournalsModule.info('等待时间：{}秒...'.format(wait_time))
        time.sleep(wait_time)
