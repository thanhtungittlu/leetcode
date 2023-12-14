from datetime import datetime

from mobio.libs.dyn.models.mongo.base_model import BaseModel


class FieldTemplate:
    MOBIO_TEMPLATE = 1


class MerchantBaseFields(BaseModel):
    def __init__(self):
        super().__init__(url_connection=None)
        self.collection = 'merchant_base_fields'

    def create_base_fields(self):
        return []

    def get_fields_by_template(self, template: int):
        result = self.get_db().find_one({"template": template})
        if not result:
            result = {
                "fields": self.create_base_fields(),
                "template": template,
                "created_time": datetime.utcnow(),
                "updated_time": datetime.utcnow()
            }
            inserted_id = self.get_db().insert_one(result)
            print('create template id: {}, inserted: {}'.format(template, inserted_id))
        for i in range(result.get('fields')):
            field = result.get('fields')[i]
            field['created_time'] = str(field.get('created_time'))
            field['updated_time'] = str(field.get('updated_time'))
            field['history'].append(
                {
                    'staff_id': 'mobio',
                    'fullname': 'mobio'.upper(),
                    'username': 'mobio'.upper(),
                    'created_time': str(field.get('created_time'))
                }
            )
            result.get('fields')[i] = field
        return result
