import datetime
import json
import uuid
from copy import copy
from bson import ObjectId
from pymongo import WriteConcern, ReadPreference


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


class JSONEncoderWithoutTz(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif type(o) == datetime.date:
            a = datetime.datetime.combine(o, datetime.datetime.min.time())
            return a.strftime("%Y-%m-%d %H:%M:%S")
        elif type(o) == datetime.datetime:
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif type(o) == datetime.time:
            return o.strftime("%H:%M:%S")
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, (bytes, bytearray)):
            return str(o, "utf-8")
        return json.JSONEncoder.default(self, o)


class BaseModel(object):
    db_name = None
    collection = None

    client_mongo = None

    def get_db(self, read_preference=None, write_concern=None):
        w = None
        if write_concern is not None:
            w = WriteConcern(w=write_concern)
        if not self.client_mongo:
            raise Exception('ERROR client_mongo: is {}'.format(self.client_mongo))
        return self.client_mongo.get_database(self.db_name).get_collection(
            self.collection, read_preference=read_preference, write_concern=w
        )

    @staticmethod
    def normalize_uuid(some_uuid):
        if isinstance(some_uuid, str):
            return uuid.UUID(some_uuid)
        return some_uuid

    def find_all(
        self,
        query,
        per_page=None,
        sort=None,
        read_preference=ReadPreference.SECONDARY_PREFERRED,
    ):
        cursor = (
            self.client_mongo.get_database(self.db_name)
            .get_collection(self.collection, read_preference=read_preference)
            .find(query)
        )
        if sort:
            cursor = cursor.sort(sort)
        if per_page:
            cursor = cursor.limit(limit=per_page)
        results = [x for x in cursor]
        return results

    def delete_one(self, query):
        return (
            self.client_mongo.get_database(self.db_name)[self.collection]
            .delete_one(query)
            .deleted_count
        )

    def delete_many(self, query):
        return (
            self.client_mongo.get_database(self.db_name)[self.collection]
            .delete_many(query)
            .deleted_count
        )

    def insert(self, data):
        d = copy(data)  # make sure that data not be modified after this function
        try:
            now = datetime.datetime.utcnow()
            d["created_time"] = now
            d["updated_time"] = now
            inserted_id = (
                self.client_mongo.get_database(self.db_name)[self.collection]
                .insert_one(d)
                .inserted_id
            )
            return inserted_id
        except Exception as ex:
            print("{} insert: {}".format(self.collection, ex))
            return None

    def update_many(self, query, data):
        return (
            self.client_mongo.get_database(self.db_name)[self.collection]
            .update_many(query, {"$set": data})
            .modified_count
        )

    def update_one(self, query, data):
        return (
            self.client_mongo.get_database(self.db_name)[self.collection]
            .update_one(query, {"$set": data})
            .matched_count
        )

    def update_one_manual(self, query, data):
        return (
            self.client_mongo.get_database(self.db_name)[self.collection]
            .update_one(query, data)
            .matched_count
        )

    def bulk_inserts(self, data):
        return (
            self.client_mongo.get_database(self.db_name)[self.collection]
            .insert_many(data)
            .inserted_ids
        )

    def find_one(self, query):
        result = (
            self.client_mongo.get_database(self.db_name)
            .get_collection(
                self.collection, read_preference=ReadPreference.SECONDARY_PREFERRED
            )
            .find_one(query)
        )
        return result

    def count(self, query):
        return (
            self.client_mongo.get_database(self.db_name)
            .get_collection(
                self.collection, read_preference=ReadPreference.SECONDARY_PREFERRED
            )
            .count(query)
        )

    def idlimit(self, query, page_size, last_id=None):
        """Function returns `page_size` number of documents after last_id
        and the new last_id.
        """
        if last_id is None:
            # When it is first page
            cursor = (
                self.client_mongo.get_database(self.db_name)[self.collection]
                .find(query)
                .sort("_id", 1)
                .limit(page_size)
            )
        else:
            tmp_query = dict(query)
            tmp_query["_id"] = {"$gt": last_id}
            # cursor = db['users'].find(tmp_query).limit(page_size)
            cursor = (
                self.client_mongo.get_database(self.db_name)[self.collection]
                .find(tmp_query)
                .sort("_id", 1)
                .limit(page_size)
            )

        # Get the data
        data = [x for x in cursor]

        if not data:
            # No documents left
            return None, None

        # Since documents are naturally ordered with _id, last document will
        # have max id.
        last_id = data[-1]["_id"]

        # Return data and last_id
        return data, last_id

    def drop_index(self, name_index):
        return self.client_mongo.get_database(self.db_name)[self.collection].drop_index(
            name_index
        )
