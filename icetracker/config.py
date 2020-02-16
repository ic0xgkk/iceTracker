import json


class Config(object):
    __instance = None
    __inited = False
    __config = dict()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        if self.__inited is True:
            return

        with open(kwargs['path'], "r", encoding='utf-8') as f:
            self.__config = json.load(f)
            f.close()

        self.__class__.__inited = True

    def get_process_list(self):
        return self.__config['process_list']


if __name__ == '__main__':
    Config(path="../config.json")
    o = Config().get_process_list()
    pass
