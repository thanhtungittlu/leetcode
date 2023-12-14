from datetime import datetime
import logging
import logging.handlers
import configparser
import time

from mobio.libs.Singleton import Singleton


class MonitorConst:
    KEY_SECTION_NAME = 'monitor'
    KEY_FILE_MAX_BYTES = 'file_max_bytes'
    KEY_FILE_BACKUP_COUNT = 'file_backup_count'
    KEY_LOG_FILE_NAME = 'log_file_name'
    KEY_FUNC_THRESHOLD = 'func_threshold'

    DEFAULT_FILE_MAX_BYTES = 10240000
    DEFAULT_FILE_BACKUP_COUNT = 10
    DEFAULT_LOG_FILE_NAME = 'monitor_slow.log'
    DEFAULT_FUNC_THRESHOLD = 0.1


@Singleton
class Monitor:
    def __init__(self):
        self.formatter = logging.Formatter('%(message)s')

        self.file_max_bytes = MonitorConst.DEFAULT_FILE_MAX_BYTES
        self.file_backup_count = MonitorConst.DEFAULT_FILE_BACKUP_COUNT
        self.log_file_name = MonitorConst.DEFAULT_LOG_FILE_NAME
        self.func_threshold = MonitorConst.DEFAULT_FUNC_THRESHOLD

        self.logger = None
        pass

    def config_from_file(self, config_file):
        """
        :param config_file: duong dan file cau hinh cho module monitor
        :return:
        """
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(config_file, encoding='utf-8')

        # check section
        has_section = config.has_section(MonitorConst.KEY_SECTION_NAME)
        if not has_section:
            raise Exception('Cannot find section %s in config file(%s). Please double check config file.' % (
                MonitorConst.KEY_SECTION_NAME, config_file))

        self.file_max_bytes = Monitor.__get_value_if_exist(config, MonitorConst.KEY_SECTION_NAME,
                                                           MonitorConst.KEY_FILE_MAX_BYTES,
                                                           MonitorConst.DEFAULT_FILE_MAX_BYTES)
        self.file_backup_count = int(Monitor.__get_value_if_exist(config, MonitorConst.KEY_SECTION_NAME,
                                                                  MonitorConst.KEY_FILE_BACKUP_COUNT,
                                                                  MonitorConst.DEFAULT_FILE_BACKUP_COUNT))
        self.log_file_name = Monitor.__get_value_if_exist(config, MonitorConst.KEY_SECTION_NAME,
                                                          MonitorConst.KEY_LOG_FILE_NAME,
                                                          MonitorConst.DEFAULT_LOG_FILE_NAME)
        self.func_threshold = float(Monitor.__get_value_if_exist(config, MonitorConst.KEY_SECTION_NAME,
                                                                 MonitorConst.KEY_FUNC_THRESHOLD,
                                                                 MonitorConst.DEFAULT_FUNC_THRESHOLD))

        self.__config()

    def config(self, file_max_bytes=MonitorConst.DEFAULT_FILE_MAX_BYTES,
               file_backup_count=MonitorConst.DEFAULT_FILE_BACKUP_COUNT,
               log_file_name=MonitorConst.DEFAULT_LOG_FILE_NAME,
               func_threshold=MonitorConst.DEFAULT_FUNC_THRESHOLD):
        """
        :param file_max_bytes: Dung lượng tối đa của file log.
        :param file_backup_count: Số lượng file log tối đa. Khi đạt só lượng file tối đa. Hệ thống sẽ quay vòng.
        :param log_file_name: Đường dẫn đến file log.
        :param func_threshold: Mức cảnh báo mặc định dùng chung. Nếu trên mức này --> ghi log.
        Có thể cấu hình riêng tuỳ biến khi sử dụng với từng function.
        :return:
        """
        self.file_max_bytes = file_max_bytes
        self.file_backup_count = file_backup_count
        self.log_file_name = log_file_name
        self.func_threshold = func_threshold

        self.__config()

    @staticmethod
    def __get_value_if_exist(config, section, key, default_value):
        """
        :param config: doi tuong configparser
        :param section: ten section trong file config. Vi du: [monitor] --> section: monitor
        :param key: key trong file config. Vi du: abc=123 --> key: abc
        :param default_value: gia tri mac dinh neu key khong ton tai trong file config.
        :return:
        """
        has_option = config.has_option(section, key)
        if not has_option:
            return default_value
        value = config.get(key)
        if not value:
            return default_value
        return value

    def __config(self, level=logging.INFO):
        self.logger = logging.getLogger('monitor')
        self.logger.setLevel(level)

        self.logger.addHandler(logging.handlers.RotatingFileHandler(filename=self.log_file_name,
                                                                    maxBytes=self.file_max_bytes,
                                                                    backupCount=self.file_backup_count))

    def monitor_func(self, threshold=-1, args_log_enable=False):
        def monitor_func_decorator(func, *args, **kwargs):
            def func_wrapper(*args1, **kwargs2):
                start_time = time.time()
                if isinstance(func, staticmethod):
                    function = func.__func__
                    result = func.__func__(*args1, **kwargs2)
                else:
                    function = func
                    result = func(*args1, **kwargs2)
                duration = time.time() - start_time
                n = threshold if threshold > 0 else self.func_threshold
                if duration > n:
                    try:
                        message = '===============================================\n'
                        message += '# Time: %s\n' % datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
                        message += '# Duration: %s\n' % '[{:.2f}s]'.format(duration)
                        message += 'Function: %s\n' % function.__name__

                        if len(args) > 0 and args_log_enable:
                            message += 'Args:\n'
                            i = 0
                            for arg in args:
                                message += '  %d: %s\n' % (i, arg)
                                i += 1
                        if len(kwargs) > 0 and args_log_enable:
                            message += 'Kwargs:\n'
                            for key, value in kwargs.items():
                                message += '  %s: %s\n' % (key, value)
                        self.logger.warn(message)
                    except Exception as ex:
                        self.logger.error('ERROR: %s' % ex)
                return result
            return func_wrapper
        return monitor_func_decorator
