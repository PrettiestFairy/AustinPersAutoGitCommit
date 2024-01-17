# coding: utf8
""" 
@File: operations.py
@Editor: PyCharm
@Author: Austin (From Chengdu.China) https://fairy.host
@HomePage: https://github.com/AustinFairyland
@OperatingSystem: Windows 11 Professional Workstation 23H2 Canary Channel
@CreatedTime: 2023-10-10
"""
from __future__ import annotations

import os
import sys
import warnings
import platform
import asyncio

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import git
import time
from datetime import datetime

from utils.publics import PublicUtilsStaticClass
from modules.journals import JournalsModule
from config import ProjectConfigClass


class OperationClass:

    def __init__(self, url_protocol: None | str):
        config_class = ProjectConfigClass()
        gitconfig = config_class.get('gitconfig')
        gitrepo = config_class.get('gitrepo')
        self.__username = gitconfig.get('username')
        if url_protocol == 'ssh':
            self.__url = gitrepo.get('giturl')
        else:
            self.__url = gitrepo.get('httpurl')
        self.__reponame = gitrepo.get('reponame')
        JournalsModule.debug(PublicUtilsStaticClass.path_root)
        self.__localrepo_path = PublicUtilsStaticClass.path_root_conver_system_separator(os.path.join(PublicUtilsStaticClass.path_root, 'data/repo'))
        if not os.path.isdir(self.__localrepo_path):
            os.mkdir(self.__localrepo_path)
        JournalsModule.debug(self.__localrepo_path)
        try:
            if os.path.isdir(self.__localrepo_path) is False:
                self.__git_clone()
            else:
                self.__repo = git.Repo(self.__localrepo_path)
                if os.path.exists(self.__localrepo_path):
                    self.__git_fetch()
        except Exception as exception:
            JournalsModule.exception(exception)
        finally:
            self.__repo = git.Repo(self.__localrepo_path)

    def __git_clone(self):
        try:
            git.Repo.clone_from(self.__url, self.__localrepo_path)
            JournalsModule.info('克隆仓库：{}'.format(self.__url))
        except Exception as exception:
            JournalsModule.exception(exception)

    def __git_fetch(self):
        try:
            self.__repo.remote().fetch()
            JournalsModule.info('远程分支提取成功')
        except Exception as exception:
            JournalsModule.exception(exception)

    def __git_commit(self, msg):
        try:
            date_format = datetime.strftime(datetime.now(), '%Y-%m-%d')
            filepath = PublicUtilsStaticClass.path_root_conver_system_separator(os.path.join(self.__localrepo_path, 'AustinPersAutoGitCommit/{}.py'.format(date_format)))
            if os.path.isfile(filepath) is False:
                file_path, file_name = os.path.split(filepath)
                if os.path.isdir(file_path) is False:
                    os.makedirs(file_path)
            with open(filepath, 'a+', encoding='utf8') as file:
                file.write('print({})\n'.format(repr('{}').format(time.time())))
            self.__repo.git.add('.')
            JournalsModule.info('暂存区添加成功')
            self.__repo.git.commit('-m', msg)
            JournalsModule.info('提交成功')
        except Exception as exception:
            JournalsModule.exception(exception)

    def __git_push(self):
        try:
            self.__repo.remotes.origin.push()
            JournalsModule.info('推送成功')
        except Exception as exception:
            JournalsModule.exception(exception)

    def commit(self, msg):
        return self.__git_commit(msg=msg)

    def push(self):
        return self.__git_push()
