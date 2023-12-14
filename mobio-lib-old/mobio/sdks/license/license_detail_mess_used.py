from .mongo_connection import BaseCollectionMongoDB
from pymongo import ReadPreference


class LicenseDetailMessUsedModel(BaseCollectionMongoDB):
    """
    Bảng lưu thông tin license_detail_mess_used
    """

    _ID = "_id"
    history_id = "history_id"
    merchant_id = "merchant_id"
    month = "month"
    mess_id = "mess_id"
    number_allow_used = "number_allow_used"
    number_used = "number_used"
    mess_type = "mess_type"
    create_on = "create_on"
    child_merchant_id = "child_merchant_id"

    mess_type_gift = "gift"
    mess_type_buy = "buy"

    def __init__(self):
        super().__init__()
        self.table_name = "license_detail_mess_used"
        self.coll_primary = self.db.get_collection(self.table_name)
        self.coll_secondary = self.db.get_collection(
            self.table_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    def insert_license_detail_mess_used(self, data_insert):
        try:
            print(
                "license_sdk::insert_license_detail_mess_used data_insert: {}".format(
                    data_insert
                )
            )
            result = self.coll_primary.insert_one(data_insert)
            if result.inserted_id is not None:
                return 1
            else:
                return 0
        except Exception as er:
            err_msg = "license_sdk insert_license_detail_mess_used ERR: {}".format(er)
            print(err_msg)
            return None

    def insert_many_license_detail_mess_used(self, data_insert):
        try:
            print(
                "license_sdk::insert_many_license_detail_mess_used data_insert: {}".format(
                    data_insert
                )
            )
            result = self.coll_primary.insert_many(data_insert)
            if result.inserted_ids is not None:
                return 1
            else:
                return 0
        except Exception as er:
            err_msg = "license_sdk insert_many_license_detail_mess_used ERR: {}".format(
                er
            )
            print(err_msg)
            return None

    def get_number_mess_used_from_mess_id(self, merchant_id, list_mess_id):
        data_used = dict()
        try:
            obj_match = {
                self.merchant_id: merchant_id,
            }
            if list_mess_id:
                obj_match.update({self.mess_id: {"$in": list_mess_id}})
            else:
                return {}
            cursor = self.coll_secondary.find(obj_match, {self._ID: 0})
            for item in cursor:
                mess_id = item.get(self.mess_id)
                data_used[mess_id] = data_used.get(mess_id, 0) + item.get(
                    self.number_used, 0
                )
        except Exception as er:
            err_msg = "license_sdk get_number_mess_used_from_mess_id ERR: {}".format(er)
            print(err_msg)
        print(
            "license_sdk::get_number_mess_used_from_mess_id data_used: {}".format(
                data_used
            )
        )
        return data_used
