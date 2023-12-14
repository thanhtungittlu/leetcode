# -*- coding: utf-8 -*-
from pymongo import MongoClient


def create_db(url_connection):
    print("create_db: ok")

    try:
        client = MongoClient(url_connection, connect=False)
    except Exception as ex:
        print('BaseModel::create_db: %r', ex)
        client = None

    return client


class DBManager:
    __instance = None

    @staticmethod
    def get_instance(url_connection):
        """ Static access method. """
        if DBManager.__instance is None:
            DBManager(url_connection)
        return DBManager.__instance

    def __init__(self, url_connection):
        """ Virtually private constructor. """
        if DBManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            print("DBManager: init call")
            DBManager.__instance = self
            self.db = create_db(url_connection)
