import uuid

from bson import ObjectId

from mobio.libs.dyn.models.mongo.db_manager import DBManager


class BaseModel(object):
    # client_mongo = None
    # db_name = sys_conf.get_section_map('mongo')['db_name']
    db_name = 'profiling'
    url_connection = None
    collection = None

    db = None

    def __init__(self, url_connection, db_name=None):
        if db_name:
            self.db_name = db_name
        self.url_connection = url_connection
        self.client_mongo = DBManager.get_instance(self.url_connection).db

    def get_db(self, read_preference=None):
        if not self.client_mongo:
            self.client_mongo = DBManager.get_instance(self.url_connection).db
        return self.client_mongo.get_database(self.db_name).get_collection(self.collection,
                                                                           read_preference=read_preference)

    @staticmethod
    def normalize_uuid(some_uuid):
        if isinstance(some_uuid, str):
            return uuid.UUID(some_uuid)
        return some_uuid

    @staticmethod
    def normalize_object_id(some_object_id):
        if isinstance(some_object_id, str):
            return ObjectId(some_object_id)
        return some_object_id
