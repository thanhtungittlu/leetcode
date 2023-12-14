from datetime import datetime
from random import randint
from time import time
from unidecode import unidecode
from mobio.libs.dyn.controllers.base_controller import BaseController
from mobio.libs.dyn.models.mongo import DynamicFieldStructure, DisplayType, DynamicFieldProperty, DynamicFieldGroup, DynamicFieldStatus, DynamicFieldStructureV2
from mobio.libs.dyn.models.mongo.merchant_config import DATE_PICKER_FORMAT, MERCHANT_CONFIG_COMMON, MerchantConfig
import re


class DynamicFieldsController(BaseController):

    @staticmethod
    def convert_field_name_2_field_key(field_name):
        time_stamp = int(round(time() * 1000))
        return "{}_{}_{}".format(MERCHANT_CONFIG_COMMON.PREFIX_DYNAMIC_FIELD, re.sub('[^a-zA-Z0-9]|\\s+', '_', unidecode(field_name)), time_stamp).lower()

    @staticmethod
    def convert_field_name_2_field_key_v2(field_name):
        time_stamp = int(round(time() * 1000))
        return "{}_{}_{}".format(MERCHANT_CONFIG_COMMON.PREFIX_DYNAMIC_FIELD, re.sub('[^a-zA-Z0-9]|\\s+', '_', unidecode(field_name[0].get('value'))), time_stamp).lower()

    def __create_history_dynamic(self, dynamic_field):
        dynamic_field[DynamicFieldStructure.HISTORY] = dynamic_field.get(DynamicFieldStructure.HISTORY) or []
        # history = {
        #     'staff_id': self.get_staff_id_from_jwt(),
        #     'fullname': self.get_value_from_jwt_by_key('fullname') or "Unknown",
        #     'username': self.get_value_from_jwt_by_key('username') or "Unknown",
        #     'created_time': datetime.utcnow()
        # }
        # dynamic_field[DynamicFieldStructure.HISTORY].append(history)
        return dynamic_field[DynamicFieldStructure.HISTORY]

    def __validate_selected_data(self, data_selected):
        is_valid = True
        for d in data_selected:
            try:
                int(d.get('id'))
                if len(d.get('name')) < 1:
                    raise Exception('name: {} is null or empty'.format(d.get('name')))
                if type(d.get('display_in_form')) != bool:
                    raise Exception('display_in_form: {} is not valid'.format(d.get('display_in_form')))
            except Exception as ex:
                print('__validate_selected_data error: {}'.format(ex))
                is_valid = False
                break
        return is_valid

    def generate_field(self, field_name, field_property, display_type, description=None, data_selected=None, datetime_format=None, display_in_form=True, order=None):
        dynamic_field_insert = dict()
        created_time = datetime.utcnow()
        field_name = field_name.strip()
        dynamic_field_insert[DynamicFieldStructure.FIELD_NAME] = field_name
        field_key = self.convert_field_name_2_field_key(field_name=field_name)
        dynamic_field_insert[DynamicFieldStructure.FIELD_KEY] = field_key
        if field_property not in [DynamicFieldProperty.INTEGER, DynamicFieldProperty.STRING, DynamicFieldProperty.DATETIME]:
            print('field_property: {} is not valid'.format(field_property))
            return None
        dynamic_field_insert[DynamicFieldStructure.FIELD_PROPERTY] = field_property
        if str(display_type) not in [str(s.value) for s in DisplayType]:
            print('display_type: {} is not valid'.format(display_type))
            return None
        dynamic_field_insert[DynamicFieldStructure.DISPLAY_TYPE] = display_type

        if display_type in [DisplayType.DROPDOWN_SINGLE_LINE, DisplayType.DROPDOWN_MULTI_LINE, DisplayType.RADIO_SELECT, DisplayType.CHECKBOX]:
            if data_selected and self.__validate_selected_data(data_selected):
                dynamic_field_insert[DynamicFieldStructure.DATA_SELECTED] = MerchantConfig.sort_id_data(data_selected)
            else:
                dynamic_field_insert[DynamicFieldStructure.DATA_SELECTED] = []
        if display_type == DisplayType.DATE_PICKER:
            if datetime_format and datetime_format in [x.get('key') for x in DATE_PICKER_FORMAT]:
                dynamic_field_insert[DynamicFieldStructure.FORMAT] = datetime_format
            else:
                print('datetime_format: {} is not valid'.format(datetime_format))
                return None
        dynamic_field_insert[DynamicFieldStructure.STATUS] = DynamicFieldStatus.ENABLE
        dynamic_field_insert[DynamicFieldStructure.DESCRIPTION] = description
        dynamic_field_insert[DynamicFieldStructure.IS_BASE] = False
        dynamic_field_insert[DynamicFieldStructure.DISPLAY_IN_FORM] = display_in_form
        # dynamic_field_insert[DynamicFieldStructure.ORDER] = max([x.get(DynamicFieldStructure.ORDER) for x in merchant_config.get(MerchantConfigStructure.DYNAMIC_FIELDS)]) + 1
        if order and type(order) == int and order > 0:
            dynamic_field_insert[DynamicFieldStructure.ORDER] = order
        else:
            dynamic_field_insert[DynamicFieldStructure.ORDER] = randint(80, 200)

        dynamic_field_insert[DynamicFieldStructure.GROUP] = DynamicFieldGroup.DYNAMIC
        dynamic_field_insert[DynamicFieldStructure.DISPLAY_IN_FORM_INPUT] = True
        dynamic_field_insert[DynamicFieldStructure.CHOOSE_DISPLAY_FROM_INPUT] = True
        dynamic_field_insert[DynamicFieldStructure.SUPPORT_SORT] = True
        dynamic_field_insert[DynamicFieldStructure.DISPLAY_IN_DB] = False
        dynamic_field_insert[DynamicFieldStructure.DISABLE_REMOVE_FORM_INPUT] = False
        dynamic_field_insert[DynamicFieldStructure.REQUIRED] = False
        dynamic_field_insert[DynamicFieldStructure.CREATED_TIME] = created_time
        dynamic_field_insert[DynamicFieldStructure.UPDATED_TIME] = created_time
        dynamic_field_insert[DynamicFieldStructure.HISTORY] = self.__create_history_dynamic(dynamic_field_insert)
        dynamic_field_insert[DynamicFieldStructure.TRANSLATE_KEY] = ''
        return dynamic_field_insert

    def __validate_localization(self, array_data):
        is_valid = True
        if not array_data:
            is_valid = False
        for data in array_data:
            try:
                if 'value' not in data or not str(data.get('value')) or len(data.get('value')) > 100:
                    is_valid = False
                if 'language' not in data or not str(data.get('language')) or len(data.get('language')) > 10:
                    is_valid = False
            except Exception as ex:
                print('__validate_localization: {}'.format(ex))
                is_valid = False
        return is_valid

    def generate_field_v2(self, field_name, field_property, display_type, description=None, data_selected=None, datetime_format=None, order=None, enable_import=True, enable_export=True, enable_edit=True, enable_add=True, enable_dashboard=True):
        if not self.__validate_localization(field_name):
            raise Exception('field name: {} is not valid'.format(field_name))
        if not self.__validate_localization(description):
            raise Exception('description: {} is not valid'.format(description))
        dynamic_field_insert = dict()
        created_time = datetime.utcnow()
        field_name = field_name
        dynamic_field_insert[DynamicFieldStructureV2.FIELD_NAME] = field_name
        field_key = self.convert_field_name_2_field_key_v2(field_name=field_name)
        dynamic_field_insert[DynamicFieldStructureV2.FIELD_KEY] = field_key
        if field_property not in [DynamicFieldProperty.INTEGER, DynamicFieldProperty.STRING, DynamicFieldProperty.DATETIME, DynamicFieldProperty.FLOAT]:
            print('field_property: {} is not valid'.format(field_property))
            return None
        dynamic_field_insert[DynamicFieldStructureV2.FIELD_PROPERTY] = field_property
        if str(display_type) not in [str(s.value) for s in DisplayType]:
            print('display_type: {} is not valid'.format(display_type))
            return None
        dynamic_field_insert[DynamicFieldStructureV2.DISPLAY_TYPE] = display_type

        if display_type in [DisplayType.DROPDOWN_SINGLE_LINE, DisplayType.DROPDOWN_MULTI_LINE, DisplayType.RADIO_SELECT, DisplayType.CHECKBOX]:
            if data_selected and self.__validate_selected_data(data_selected):
                dynamic_field_insert[DynamicFieldStructureV2.DATA_SELECTED] = MerchantConfig.sort_id_data(data_selected)
            else:
                dynamic_field_insert[DynamicFieldStructureV2.DATA_SELECTED] = []
        if display_type == DisplayType.DATE_PICKER:
            if datetime_format and datetime_format in [x.get('key') for x in DATE_PICKER_FORMAT]:
                dynamic_field_insert[DynamicFieldStructureV2.FORMAT] = datetime_format
            else:
                print('datetime_format: {} is not valid'.format(datetime_format))
                return None
        dynamic_field_insert[DynamicFieldStructureV2.STATUS] = DynamicFieldStatus.ENABLE
        dynamic_field_insert[DynamicFieldStructureV2.DESCRIPTION] = description
        dynamic_field_insert[DynamicFieldStructureV2.IS_BASE] = False
        dynamic_field_insert[DynamicFieldStructureV2.VIEW_ALL] = True
        # dynamic_field_insert[DynamicFieldStructureV2.ORDER] = max([x.get(DynamicFieldStructureV2.ORDER) for x in merchant_config.get(MerchantConfigStructure.DYNAMIC_FIELDS)]) + 1
        if order and type(order) == int and order > 0:
            dynamic_field_insert[DynamicFieldStructureV2.ORDER] = order
        else:
            dynamic_field_insert[DynamicFieldStructureV2.ORDER] = randint(80, 200)

        dynamic_field_insert[DynamicFieldStructureV2.GROUP] = DynamicFieldGroup.DYNAMIC
        dynamic_field_insert[DynamicFieldStructureV2.FILTER] = True
        dynamic_field_insert[DynamicFieldStructureV2.SUPPORT_SORT] = True
        dynamic_field_insert[DynamicFieldStructureV2.REQUIRED] = False
        dynamic_field_insert[DynamicFieldStructureV2.CREATED_TIME] = created_time
        dynamic_field_insert[DynamicFieldStructureV2.UPDATED_TIME] = created_time
        dynamic_field_insert[DynamicFieldStructureV2.HISTORY] = self.__create_history_dynamic(dynamic_field_insert)
        dynamic_field_insert[DynamicFieldStructureV2.TRANSLATE_KEY] = ''

        # # Set DISPLAY
        # Dashboard
        dynamic_field_insert[DynamicFieldStructureV2.DASHBOARD_LEFT] = enable_dashboard
        dynamic_field_insert[DynamicFieldStructureV2.DASHBOARD_RIGHT] = enable_dashboard
        dynamic_field_insert[DynamicFieldStructureV2.DISABLE_REMOVE_DASHBOARD] = False
        # Export
        dynamic_field_insert[DynamicFieldStructureV2.EXPORT_LEFT] = enable_export
        dynamic_field_insert[DynamicFieldStructureV2.EXPORT_RIGHT] = enable_export
        dynamic_field_insert[DynamicFieldStructureV2.DISABLE_REMOVE_EXPORT] = False
        # Import
        dynamic_field_insert[DynamicFieldStructureV2.IMPORT_LEFT_INPUT] = enable_import
        dynamic_field_insert[DynamicFieldStructureV2.IMPORT_RIGHT_INPUT] = enable_import
        dynamic_field_insert[DynamicFieldStructureV2.DISABLE_REMOVE_IMPORT] = False
        # Add
        dynamic_field_insert[DynamicFieldStructureV2.ADD_LEFT_INPUT] = enable_add
        dynamic_field_insert[DynamicFieldStructureV2.ADD_RIGHT_INPUT] = enable_add
        dynamic_field_insert[DynamicFieldStructureV2.DISABLE_REMOVE_ADD_INPUT] = False
        # Edit
        dynamic_field_insert[DynamicFieldStructureV2.EDIT_LEFT_INPUT] = enable_edit
        dynamic_field_insert[DynamicFieldStructureV2.EDIT_RIGHT_INPUT] = enable_edit
        dynamic_field_insert[DynamicFieldStructureV2.DISABLE_REMOVE_EDIT_INPUT] = False

        return dynamic_field_insert
