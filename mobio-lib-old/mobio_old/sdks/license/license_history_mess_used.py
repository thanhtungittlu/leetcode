from .mongo_connection import BaseCollectionMongoDB
from pymongo import ReadPreference


class LicenseHistoryMessUsedModel(BaseCollectionMongoDB):
    """
    Bảng lưu thông tin license_history_mess_used
    """

    _ID = "_id"
    history_id = "history_id"
    merchant_id = "merchant_id"
    month = "month"
    mess_increase_used = "mess_increase_used"
    mess_base_used = "mess_base_used"
    gift_used = "gift_used"
    mess_base = "mess_base"
    mess_increase = "mess_increase"
    gift = "gift"
    mess_surplus = "mess_surplus"
    create_on = "create_on"
    child_merchant_id = "child_merchant_id"

    def __init__(self):
        super().__init__()
        self.table_name = "license_history_mess_used"
        self.coll_primary = self.db.get_collection(self.table_name)
        self.coll_secondary = self.db.get_collection(
            self.table_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    def insert_license_history_mess_used(self, data_insert):
        try:
            print(
                "license_sdk::insert_license_history_mess_used data_insert: {}".format(
                    data_insert
                )
            )
            result = self.coll_primary.insert_one(data_insert)
            if result.inserted_id is not None:
                return 1
            else:
                return 0
        except Exception as er:
            err_msg = "license_sdk insert_license_history_mess_used ERR: {}".format(er)
            print(err_msg)
            return None
