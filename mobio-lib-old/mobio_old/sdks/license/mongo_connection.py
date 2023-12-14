from pymongo import MongoClient

from .config import Mongo

global_admin_mongodb_client = None


class MongoDBInit(object):
    @staticmethod
    def mongodb_init():
        global global_admin_mongodb_client
        if global_admin_mongodb_client is None:
            global_admin_mongodb_client = MongoClient(Mongo.ADMIN_MONGO_DB)
        return global_admin_mongodb_client


class BaseMongoDB(object):
    def __init__(self, mongo_client, db_name):
        self.client = mongo_client
        self.db = self.client.get_database(db_name)
        self.coll_primary = None
        self.coll_secondary = None


class BaseCollectionMongoDB(BaseMongoDB):
    def __init__(self):
        super(BaseCollectionMongoDB, self).__init__(
            mongo_client=MongoDBInit.mongodb_init(),
            db_name=Mongo.ADMIN_MONGO_DB_DB_NAME,
        )
