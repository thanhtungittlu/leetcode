import uuid
from copy import deepcopy
from datetime import datetime

from mobio.libs.dyn.helpers.merchant_config_helper import MerchantConfigHelper
from mobio.libs.dyn.models.mongo import MerchantConfigStructure, DynamicFieldStructureV2, LIST_FIELDS_SUPPORT_SORT
from mobio.libs.dyn.models.mongo.base_model import BaseModel
from mobio.libs.dyn.models.mongo.merchant_base_fields import MerchantBaseFields
from mobio.libs.dyn.models.mongo.staff_display_fields import StaffDisplayFields


class MERCHANT_CONFIG_COMMON:
    PREFIX_DYNAMIC_FIELD = '_dyn'
    PREFIX_CRITERIA = 'cri'
    MERCHANT_CONFIG_CURRENT_VERSION = 0.1


DATE_PICKER_FORMAT = [
    {
        "key": 'dd/mm',
        "format": "%d/%m",
        "alternate_format": "%d-%m",
        "year": 2099
    },
    {
        "key": 'dd/mm/yyyy',
        "format": "%d/%m/%Y",
        "alternate_format": "%d-%m-%Y",
        "year": None
    },
    {
        "key": 'dd/mm/yyyy hh:mm',
        "format": "%d/%m/%Y %H:%M",
        "alternate_format": "%d-%m-%Y %H:%M",
        "year": None
    }
]


class MerchantConfig(BaseModel):
    def __init__(self):
        super().__init__(url_connection=None)
        self.collection = 'merchant_config'

    def generate_merchant_config(self, merchant_id):
        merchant_id = self.normalize_uuid(merchant_id)
        data = {
            MerchantConfigStructure.MERCHANT_ID: merchant_id,
            MerchantConfigStructure.CREATED_TIME: datetime.utcnow(),
            MerchantConfigStructure.DYNAMIC_FIELDS: [],
            MerchantConfigStructure.PARENTS: [],
            'field_template': 1,
            MerchantConfigStructure.TIMEZONE: "Asia/Ho_Chi_Minh",
            MerchantConfigStructure.VERSION: 0.1
        }
        return data

    def get_merchant_config(self, merchant_id, selected_data=False, staff_id=None):
        merchant_id = self.normalize_uuid(merchant_id)
        result = self.get_db().find_one({'merchant_id': merchant_id})
        if result is None:
            data = self.generate_merchant_config(merchant_id)
            result_insert = self.get_db().insert_one(data)
            result = data
            result['_id'] = result_insert.inserted_id
        else:
            need_update = False
            if result.get(MerchantConfigStructure.VERSION) < MERCHANT_CONFIG_COMMON.MERCHANT_CONFIG_CURRENT_VERSION:
                result = MerchantConfigHelper().update_merchant_config(result, MERCHANT_CONFIG_COMMON.MERCHANT_CONFIG_CURRENT_VERSION)
                need_update = True
            if need_update:
                result[MerchantConfigStructure.UPDATED_TIME] = datetime.utcnow().timestamp()
                result_update = self.get_db().update_one({"_id": result.get('_id')}, {'$set': {i: result[i] for i in result if i != '_id'}})
        base_fields = MerchantBaseFields().get_fields_by_template(result.get('field_template') or 1)
        merchant_fields = result.get(MerchantConfigStructure.DYNAMIC_FIELDS) or []
        merchant_fields.extend(base_fields)

        staff_display_fields = StaffDisplayFields().get_fields_by_staff(str(staff_id)) if staff_id else {}
        tmp_fields = list()
        for field in merchant_fields:
            if staff_display_fields:
                if staff_display_fields.get('dashboard'):
                    staff_display_db = next((x for x in staff_display_fields.get('dashboard') if field.get(DynamicFieldStructureV2.FIELD_KEY) == x.get(DynamicFieldStructureV2.FIELD_KEY)), None)
                    if staff_display_db:
                        field[DynamicFieldStructureV2.DASHBOARD_LEFT] = True
                        field[DynamicFieldStructureV2.DASHBOARD_RIGHT] = True
                        field[DynamicFieldStructureV2.DB_ORDER] = staff_display_db.get(DynamicFieldStructureV2.DB_ORDER)
                    else:
                        field[DynamicFieldStructureV2.DASHBOARD_LEFT] = False
                        field[DynamicFieldStructureV2.DASHBOARD_RIGHT] = False

                if staff_display_fields.get('export'):
                    staff_display_export = next((x for x in staff_display_fields.get('export') if field.get(DynamicFieldStructureV2.FIELD_KEY) == x.get(DynamicFieldStructureV2.FIELD_KEY)), None)
                    if staff_display_export:
                        field[DynamicFieldStructureV2.EXPORT_LEFT] = True
                        field[DynamicFieldStructureV2.EXPORT_RIGHT] = True
                        field[DynamicFieldStructureV2.ORDER] = staff_display_export.get(DynamicFieldStructureV2.ORDER)
                    else:
                        field[DynamicFieldStructureV2.EXPORT_LEFT] = False
                        field[DynamicFieldStructureV2.EXPORT_RIGHT] = False

                if staff_display_fields.get('import'):
                    staff_display_import = next((x for x in staff_display_fields.get('import') if field.get(DynamicFieldStructureV2.FIELD_KEY) == x.get(DynamicFieldStructureV2.FIELD_KEY)), None)
                    if staff_display_import:
                        field[DynamicFieldStructureV2.IMPORT_LEFT_INPUT] = True
                        field[DynamicFieldStructureV2.IMPORT_RIGHT_INPUT] = True
                        field[DynamicFieldStructureV2.ORDER] = staff_display_import.get(DynamicFieldStructureV2.ORDER)
                    else:
                        field[DynamicFieldStructureV2.IMPORT_LEFT_INPUT] = False
                        field[DynamicFieldStructureV2.IMPORT_RIGHT_INPUT] = False

                if staff_display_fields.get('add_input'):
                    staff_display_add = next((x for x in staff_display_fields.get('add_input') if field.get(DynamicFieldStructureV2.FIELD_KEY) == x.get(DynamicFieldStructureV2.FIELD_KEY)), None)
                    if staff_display_add:
                        field[DynamicFieldStructureV2.ADD_LEFT_INPUT] = True
                        field[DynamicFieldStructureV2.ADD_RIGHT_INPUT] = True
                        field[DynamicFieldStructureV2.ORDER] = staff_display_add.get(DynamicFieldStructureV2.ORDER)
                        field[DynamicFieldStructureV2.REQUIRED] = staff_display_add.get(DynamicFieldStructureV2.REQUIRED)
                    else:
                        field[DynamicFieldStructureV2.ADD_LEFT_INPUT] = False
                        field[DynamicFieldStructureV2.ADD_RIGHT_INPUT] = False

                if staff_display_fields.get('edit_input'):
                    staff_display_edit = next((x for x in staff_display_fields.get('edit_input') if field.get(DynamicFieldStructureV2.FIELD_KEY) == x.get(DynamicFieldStructureV2.FIELD_KEY)), None)
                    if staff_display_edit:
                        field[DynamicFieldStructureV2.EDIT_LEFT_INPUT] = True
                        field[DynamicFieldStructureV2.EDIT_RIGHT_INPUT] = True
                        field[DynamicFieldStructureV2.ORDER] = staff_display_edit.get(DynamicFieldStructureV2.ORDER)
                        field[DynamicFieldStructureV2.REQUIRED] = staff_display_edit.get(DynamicFieldStructureV2.REQUIRED)
                    else:
                        field[DynamicFieldStructureV2.EDIT_LEFT_INPUT] = False
                        field[DynamicFieldStructureV2.EDIT_RIGHT_INPUT] = False

            if field.get(DynamicFieldStructureV2.FIELD_KEY).startswith(MERCHANT_CONFIG_COMMON.PREFIX_DYNAMIC_FIELD) or field.get(DynamicFieldStructureV2.FIELD_KEY) in LIST_FIELDS_SUPPORT_SORT:
                field[DynamicFieldStructureV2.SUPPORT_SORT] = True
            else:
                field[DynamicFieldStructureV2.SUPPORT_SORT] = False
            tmp_fields.append(field)
        merchant_fields = deepcopy(tmp_fields)
        del tmp_fields
        result[MerchantConfigStructure.DYNAMIC_FIELDS] = merchant_fields
        return result

    def update_merchant(self, merchant_config):
        if "_id" in merchant_config:
            result_update = self.get_db().update_one({"_id": merchant_config.get('_id')}, {'$set': {i: merchant_config[i] for i in merchant_config if i != '_id'}}, upsert=True)
        else:
            result_update = self.get_db().update_one({"merchant_id": merchant_config.get('merchant_id')}, {'$set': {i: merchant_config[i] for i in merchant_config if i != '_id'}}, upsert=True)
        return result_update.matched_count

    def check_merchant_exists(self, merchant_id):
        merchant_id = uuid.UUID(merchant_id) if type(merchant_id) == str else merchant_id
        result = self.get_db().find_one({'merchant_id': merchant_id})
        return result

    @staticmethod
    def sort_id_data(data):
        sort_by_key = ['id']
        new_data = []
        set_data = set()
        tmp_data = []
        for row in data:
            if row.get('name') not in set_data:
                tmp_data.append(row)
                set_data.add(row.get('name'))
        data = tmp_data
        data = sorted(data, key=lambda k: tuple([k[x] for x in sort_by_key]))

        for i in data:
            i['id'] = max([x.get('id') for x in new_data]) + 1 if i.get('id') in [x.get('id') for x in new_data] else i.get('id')
            new_data.append(i)
        return new_data
