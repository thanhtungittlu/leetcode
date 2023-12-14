import datetime
import json
import uuid

from bson import ObjectId

from mobio.libs.m_scheduler_partitioning.scheduler_models.db_manager import DBManager


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif type(o) == datetime.date:
            a = datetime.datetime.combine(o, datetime.datetime.min.time())
            return a.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        elif type(o) == datetime.datetime:
            return o.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, (bytes, bytearray)):
            return str(o, "utf-8")
        return json.JSONEncoder.default(self, o)


class BaseModel(object):
    CREATED_TIME = "created_time"
    UPDATED_TIME = "updated_time"

    db_name = "test"
    url_connection = None
    collection = None

    db = None

    def __init__(self, url_connection):
        self.url_connection = url_connection
        self.client_mongo = DBManager.get_instance(self.url_connection).db
        self.db_name = self.client_mongo.get_database().name

    def get_db(self, read_preference=None):
        if not self.client_mongo:
            self.client_mongo = DBManager.get_instance(self.url_connection).db
        return self.client_mongo.get_database(self.db_name).get_collection(
            self.collection, read_preference=read_preference
        )

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
