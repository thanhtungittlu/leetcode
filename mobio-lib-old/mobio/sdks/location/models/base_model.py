import datetime
import json
import uuid

from bson import ObjectId, Decimal128
from pymongo import ReadPreference, WriteConcern
from .db_manager import DBManager


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
        elif isinstance(o, Decimal128):
            return str(o)
        return json.JSONEncoder.default(self, o)


class BaseModel(object):
    db_name = None
    collection = None

    client_mongo = DBManager.get_instance().db

    def get_db(self, read_preference=None, write_concern=None):
        w = None
        if write_concern is not None:
            w = WriteConcern(w=write_concern)
        if not self.client_mongo:
            raise Exception('ERROR client_mongo: is {}'.format(self.client_mongo))
        return self.client_mongo.get_database(self.db_name).get_collection(
            self.collection, read_preference=read_preference, write_concern=w
        )

    def find_one(self, query, sort=None):
        if sort:
            result = (
                self.client_mongo.get_database().get_collection(
                    self.collection, read_preference=ReadPreference.SECONDARY_PREFERRED
                ).find_one(query, sort=sort)
            )
        else:
            result = (
                self.client_mongo.get_database().get_collection(
                    self.collection, read_preference=ReadPreference.SECONDARY_PREFERRED
                ).find_one(query)
            )
        return result

    def find_all(
            self,
            query,
            per_page=None,
            sort=None,
            read_preference=ReadPreference.SECONDARY_PREFERRED,
    ):
        cursor = (
            self.client_mongo.get_database().get_collection(self.collection, read_preference=read_preference)
                .find(query)
        )
        if sort:
            cursor = cursor.sort(sort)
        if per_page:
            cursor = cursor.limit(limit=per_page)
        results = [x for x in cursor]
        return json.loads(JSONEncoder().encode(results)) if len(results) > 0 else []
