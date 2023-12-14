#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 19/03/2021
"""
import io
import logging
import os
import sys
import traceback

from mobio.libs.Singleton import Singleton
from mobio.sdks.base.common import CONSTANTS
from mobio.sdks.base.common.system_config import SystemConfig
from mobio.sdks.base.configs import LoggingConfig, ApplicationConfig
from logstash_formatter import LogstashFormatterV1
from logging import DEBUG, INFO, WARNING


class LOGGING:
    WRITE_TRACEBACK_FOR_ALL_CUSTOMIZE_EXCEPTION = "write_traceback_for_all_customize_exception"
    WRITE_TRACEBACK_FOR_GLOBAL_EXCEPTION = "write_traceback_for_global_exception"
    LOG_FOR_REQUEST_SUCCESS = "log_for_request_success"
    LOG_FOR_ALL_CUSTOMIZE_EXCEPTION = "log_for_all_customize_exception"
    LOG_FOR_GLOBAL_EXCEPTION = "log_for_global_exception"
    FILE_MAX_BYTES = "file_max_bytes"
    FILE_BACKUP_COUNT = "file_backup_count"


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else:
    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


@Singleton
class MobioLogging:
    def __init__(self):
        self.name = 'MOBIO'

        self.logger = logging.getLogger(self.name)

        if not LoggingConfig.K8S:
            logging.config.fileConfig(ApplicationConfig.LOG_CONFIG_FILE_PATH, None, disable_existing_loggers=False)

            max_bytes = int(SystemConfig().get_section_map(CONSTANTS.LOGGING_MODE)[CONSTANTS.FILE_MAX_BYTES])
            backup_count = int(SystemConfig().get_section_map(CONSTANTS.LOGGING_MODE)[CONSTANTS.FILE_BACKUP_COUNT])
            if max_bytes > 0:
                try:
                    os.makedirs(os.path.dirname(ApplicationConfig.LOG_FILE_PATH), exist_ok=True)
                except Exception as ex:
                    print('WARNING:mobio_logging::__init__():make log dir: %s' % ex)
                self.logger.addHandler(logging.handlers.RotatingFileHandler(filename=ApplicationConfig.LOG_FILE_PATH,
                                                                            maxBytes=max_bytes,
                                                                            backupCount=backup_count))
        else:
            handler = logging.StreamHandler(stream=sys.stdout)
            if LoggingConfig.K8S:
                handler.setFormatter(LogstashFormatterV1())
            logging.basicConfig(handlers=[handler], level=logging.DEBUG)

    def findCaller(self, stack_info=False, stacklevel=1):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        # # On some versions of IronPython, currentframe() returns None if
        # # IronPython isn't run with -X:Frames.
        # if f is not None:
        #     f = f.f_back
        orig_f = f
        while f and stacklevel > 1:
            f = f.f_back
            stacklevel -= 1
        if not f:
            f = orig_f
        rv = "(unknown file)", 0, "(unknown function)", None
        _srcfile = os.path.abspath(__file__)
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    def warning(self, content, *args, log_key=None, **kwargs):
        if isinstance(content, dict) and LoggingConfig.K8S:
            content["log_key"] = log_key

        try:
            fn, lno, func, sinfo = self.findCaller()
        except ValueError:  # pragma: no cover
            fn, lno, func, sinfo = "(unknown file)", 0, "(unknown function)", None

        exc_info = kwargs.get('full_log', False)

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
                if exc_info[0] is None and exc_info[1] is None:
                    exc_info = False

        extra = kwargs.get('extra', None)
        record = self.logger.makeRecord(self.name, WARNING, fn, lno, content, args,
                                        exc_info, func, extra, sinfo)
        self.logger.handle(record)

    def debug(self, content, *args, log_key=None, **kwargs):
        if isinstance(content, dict) and LoggingConfig.K8S:
            content["log_key"] = log_key

        try:
            fn, lno, func, sinfo = self.findCaller()
        except ValueError:  # pragma: no cover
            fn, lno, func, sinfo = "(unknown file)", 0, "(unknown function)", None

        exc_info = kwargs.get('full_log', False)

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
                if exc_info[0] is None and exc_info[1] is None:
                    exc_info = False

        extra = kwargs.get('extra', None)
        record = self.logger.makeRecord(self.name, DEBUG, fn, lno, content, args,
                                        exc_info, func, extra, sinfo)
        self.logger.handle(record)

    def error(self, content, log_key=None):
        if isinstance(content, dict) and LoggingConfig.K8S:
            content["log_key"] = log_key
        self.logger.error(content, exc_info=True)

    def info(self, content, *args, log_key=None, **kwargs):
        if isinstance(content, dict) and LoggingConfig.K8S:
            content["log_key"] = log_key

        try:
            fn, lno, func, sinfo = self.findCaller()
        except ValueError:  # pragma: no cover
            fn, lno, func, sinfo = "(unknown file)", 0, "(unknown function)", None

        exc_info = kwargs.get('full_log', False)

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
                if exc_info[0] is None and exc_info[1] is None:
                    exc_info = False

        extra = kwargs.get('extra', None)
        record = self.logger.makeRecord(self.name, INFO, fn, lno, content, args,
                                        exc_info, func, extra, sinfo)
        self.logger.handle(record)

    def exception(self, content, log_key=None):
        if isinstance(content, dict) and LoggingConfig.K8S:
            content["log_key"] = log_key
        self.logger.exception(content)
