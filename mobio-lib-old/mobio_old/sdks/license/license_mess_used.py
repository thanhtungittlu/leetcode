from .mongo_connection import BaseCollectionMongoDB
from pymongo import ReadPreference
from .date_utils import get_utc_now, convert_date_to_format


class LicenseMessUsedModel(BaseCollectionMongoDB):
    """
    Bảng lưu thông tin license_mess_used
    """

    _ID = "_id"
    merchant_id = "merchant_id"
    month = "month"
    mess_increase_used = "mess_increase_used"
    mess_base_used = "mess_base_used"
    gift_used = "gift_used"
    mess_base = "mess_base"
    mess_increase = "mess_increase"
    gift = "gift"
    mess_surplus = "mess_surplus"
    check_sum = "check_sum"
    create_on = "create_on"
    update_on = "update_on"

    def __init__(self):
        super().__init__()
        self.table_name = "license_mess_used"
        self.coll_primary = self.db.get_collection(self.table_name)
        self.coll_secondary = self.db.get_collection(
            self.table_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    def find_one_license_mess_used(self, merchant_id, day_of_month):
        try:
            result = self.coll_secondary.find_one(
                {self.merchant_id: merchant_id, self.month: day_of_month},
                {self._ID: 0},
            )
            print("license_sdk::find_one_license_mess_used result: {}".format(result))
            return result
        except Exception as er:
            err_msg = "license_sdk find_one_license_mess_used ERR: {}".format(er)
            print(err_msg)
            return None

    def upsert_data_mess_used(self, merchant_id, day_of_month, data):
        try:
            dnow_utc = convert_date_to_format(get_utc_now())
            result = self.coll_primary.update_one(
                {self.merchant_id: merchant_id, self.month: day_of_month},
                {
                    "$set": data,
                    "$setOnInsert": {self.create_on: dnow_utc},
                },
                upsert=True,
            )
            return result.modified_count
        except Exception as er:
            err_msg = "license_sdk upsert_data_mess_used ERR: {}".format(er)
            print(err_msg)
            return None

    def data_mess_to_string(self, data_mess):
        data_str = ""
        data_str += data_mess.get(self.merchant_id, "")
        data_str += "_" + data_mess.get(self.month, "")
        data_str += "_" + str(data_mess.get(self.mess_base, 0))
        data_str += "_" + str(data_mess.get(self.mess_base_used, 0))
        data_str += "_" + str(data_mess.get(self.mess_increase, 0))
        data_str += "_" + str(data_mess.get(self.mess_increase_used, 0))
        data_str += "_" + str(data_mess.get(self.gift, 0))
        data_str += "_" + str(data_mess.get(self.gift_used, 0))
        data_str += "_" + str(data_mess.get(self.mess_surplus, 0))
        # data_str += "_" + str(data_mess.get(self.create_on, ""))
        # data_str += "_" + str(data_mess.get(self.update_on, ""))
        return data_str
