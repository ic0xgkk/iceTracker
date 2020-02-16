import sqlite3


class SQLite(sqlite3.Connection):
    __instance = None
    __inited = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):

        if self.__inited is True:
            return

        super().__init__("")

        self.__class__.__inited = True