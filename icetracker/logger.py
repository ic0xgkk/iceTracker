import logging
import time
import os


class Logger(logging.Logger):
    __instance = None
    __inited = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        if self.__inited is True:
            return

        super().__init__("iceTracker")
        if not os.path.exists("./log/"):
            os.mkdir("./log/")
        log_name = './log/' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.log'
        file_header = logging.FileHandler(log_name, encoding='utf-8')
        formatter = logging.Formatter(fmt='[%(levelname)s#%(asctime)s#%(process)d#%(thread)d#'
                                              '%(module)s#%(filename)s#%(funcName)s}]%(message)s',
                                          datefmt="%Y-%m-%d %H:%M:%S,uuu")
        file_header.setFormatter(formatter)
        self.addHandler(file_header)

        self.__class__.__inited = True
