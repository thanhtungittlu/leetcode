#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class ApplicationConfig:
    BASE_HOST = str(os.environ.get("HOST"))
    APPLICATION_DATA_DIR = os.environ.get('APPLICATION_DATA_DIR')
    APPLICATION_LOGS_DIR = os.environ.get('APPLICATION_LOGS_DIR')
    MOBIO_TOKEN = os.environ.get('YEK_REWOP', '')

    CONFIG_FILE_PATH = ''
    LOG_CONFIG_FILE_PATH = ''
    LOG_FILE_PATH = ''


class LoggingConfig:
    K8S = bool(int(os.environ.get("K8S", '0')))
