# coding: utf8
""" 
@File: conf.py
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

import yaml
import os
from typing import Union

from modules.journals import JournalsModule


class ProjectConfigClass:
    """
    项目配置类
    """

    def __init__(self):
        self.__config = self.__read_config()

    def __read_config(self) -> dict:
        from utils.publics import PublicUtilsStaticClass
        try:
            config_path = PublicUtilsStaticClass.path_root_conver_system_separator(os.path.join(PublicUtilsStaticClass.path_root, 'config/config.yaml'))
            if os.path.isfile(config_path) is False:
                config_path = PublicUtilsStaticClass.path_root_conver_system_separator(os.path.join(PublicUtilsStaticClass.path_root, 'config/config.dev.yaml'))
            else:
                raise Exception
        except Exception as error:
            JournalsModule.exception(error)
        with open(config_path, 'r') as file:
            try:
                config_data = yaml.safe_load(file)
                JournalsModule.info('配置文件: {} 读取成功.'.format(config_path))
                return config_data
            except Exception as error:
                JournalsModule.exception(error)
                return None

    def get(self, key: str = None) -> Union[dict, str]:
        """
        获取配置
        :param key: 关键字 
        :return: 
        """
        if key is None:
            return self.__config
        else:
            return self.__config.get(key)
