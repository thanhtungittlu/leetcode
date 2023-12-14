# -*- coding: utf-8 -*-
import os
from pymongo import MongoClient


def create_db():
    print("create_db: ok")

    try:
        url_connection = os.getenv("LOCATION_MONGO_URI")
        client = MongoClient(url_connection, connect=False)
    except Exception as ex:
        print('BaseModel::create_db: %r', ex)
        client = None

    return client


class DBManager:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DBManager.__instance is None:
            DBManager()
        return DBManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DBManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            print("DBManager: init call")
            DBManager.__instance = self
            self.db = create_db()
