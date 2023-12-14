#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: MOBIO
    Date created: 2019/03/01
"""
import configparser
import logging.config

from mobio.libs.Singleton import Singleton
from mobio.sdks.base.configs import ApplicationConfig


@Singleton
class SystemConfig:
    config = configparser.ConfigParser()
    _sections = {}

    def __init__(self):
        self.config.read(ApplicationConfig.CONFIG_FILE_PATH, 'utf-8')

    def get_section_map(self, section):
        if section in self._sections:
            return self._sections[section]

        local_dic = {}
        options = self.config.options(section)
        for option in options:
            try:
                local_dic[option] = self.config.get(section, option)
                if local_dic[option] == -1:
                    print("INFO:MOBIO:SystemConfig.get_section_map():skip: %s" % option)
            except Exception as e:
                print("ERROR:MOBIO::SystemConfig.get_section_map():section: %s" % section)
                print("ERROR:MOBIO::SystemConfig.get_section_map():option: %s" % option)
                print("ERROR:MOBIO::SystemConfig.get_section_map():error: %s" % e)
                local_dic[option] = None
        self._sections[section] = local_dic
        return local_dic
