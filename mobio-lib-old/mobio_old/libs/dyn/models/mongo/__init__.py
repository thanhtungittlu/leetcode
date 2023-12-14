import inspect
from enum import Enum

LIST_FIELDS_SUPPORT_SORT = []


class MerchantConfigStructure:
    CREATED_TIME = 'created_time'
    UPDATED_TIME = 'updated_time'
    MERCHANT_ID = 'merchant_id'
    DYNAMIC_FIELDS = 'dynamic_fields'
    PARENTS = 'parents'
    TIMEZONE = 'timezone'
    VERSION = 'version'


class DynamicFieldStructure:
    FIELD_ID = 'field_id'
    FIELD_NAME = 'field_name'
    FIELD_KEY = 'field_key'
    FIELD_PROPERTY = 'field_property'
    DISPLAY_TYPE = 'display_type'
    DATA_SELECTED = 'data_selected'
    FORMAT = 'format'
    GROUP = 'group'
    DISPLAY_IN_FORM = 'display_in_form'
    DISPLAY_IN_DB = 'display_in_dashboard'
    DB_ORDER = 'dashboard_order'
    DISABLE_REMOVE_DASHBOARD = 'disable_remove_dashboard'
    CHOOSE_DISPLAY_FROM_INPUT = 'choose_display_form_input'
    DISPLAY_IN_FORM_INPUT = 'display_in_form_input'
    ORDER = 'order'
    DISABLE_REMOVE_FORM_INPUT = 'disable_remove_form_input'
    REQUIRED = 'required'
    HISTORY = 'history'
    LAST_UPDATE_BY = 'last_update_by'
    IS_BASE = 'is_base'
    STATUS = 'status'
    TRANSLATE_KEY = 'translate_key'
    SUPPORT_SORT = 'support_sort'
    DESCRIPTION = 'description'
    CREATED_TIME = 'created_time'
    UPDATED_TIME = 'updated_time'


class DynamicFieldStructureV2:
    FIELD_ID = 'field_id'
    FIELD_NAME = 'field_name'
    FIELD_KEY = 'field_key'
    FIELD_PROPERTY = 'field_property'
    DISPLAY_TYPE = 'display_type'
    DATA_SELECTED = 'data_selected'
    FORMAT = 'format'
    GROUP = 'group'
    DB_ORDER = 'dashboard_order'
    ORDER = 'order'
    REQUIRED = 'required'
    HISTORY = 'history'
    LAST_UPDATE_BY = 'last_update_by'
    IS_BASE = 'is_base'
    STATUS = 'status'
    TRANSLATE_KEY = 'translate_key'
    SUPPORT_SORT = 'support_sort'
    FILTER = 'filter'
    DESCRIPTION = 'description'
    CREATED_TIME = 'created_time'
    UPDATED_TIME = 'updated_time'
    VIEW_ALL = 'view_all'
    DASHBOARD_LEFT = 'dashboard_left'
    DASHBOARD_RIGHT = 'dashboard_right'
    DISABLE_REMOVE_DASHBOARD = 'disable_remove_dashboard'
    EXPORT_LEFT = 'export_left_input'
    EXPORT_RIGHT = 'export_right_input'
    DISABLE_REMOVE_EXPORT = 'disable_remove_export'
    IMPORT_LEFT_INPUT = 'import_left_input'
    IMPORT_RIGHT_INPUT = 'import_right_input'
    DISABLE_REMOVE_IMPORT = 'disable_remove_import'
    ADD_LEFT_INPUT = 'add_left_input'
    ADD_RIGHT_INPUT = 'add_right_input'
    DISABLE_REMOVE_ADD_INPUT = 'disable_remove_add_input'
    EDIT_RIGHT_INPUT = 'edit_right_input'
    EDIT_LEFT_INPUT = 'edit_left_input'
    DISABLE_REMOVE_EDIT_INPUT = 'disable_remove_edit_input'


class DynamicFieldProperty:
    INTEGER = 1
    FLOAT = 4
    STRING = 2
    DATETIME = 3
    # LIST = 5
    DICT = 5
    EMAIL = 6
    PHONE_NUMBER = 7
    GENDER = 8
    # PROVINCE = 9
    # DISTRICT = 10
    # WARD = 11
    RELATIONSHIP_DATA = 9
    RELATION_WITH_CHILDS = 10
    CHILDS = 11
    SOCIAL_TAGS = 12
    SOCIAL_USER = 13
    UDT = 14
    CARDS = 15
    PUSH_ID = 16

    @classmethod
    def get_all_property(cls):
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        values = [a[1] for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
        return values


class DisplayType(Enum):
    SINGLE_LINE = 'single_line'
    MULTI_LINE = 'multi_line'
    DROPDOWN_SINGLE_LINE = 'dropdown_single_line'
    DROPDOWN_MULTI_LINE = 'dropdown_multi_line'
    RADIO_SELECT = 'radio'
    CHECKBOX = 'checkbox'
    DATE_PICKER = 'date_picker'
    TAGS = 'tags'


class DynamicFieldGroup:
    INFORMATION = 'information'
    DEMOGRAPHIC = 'demographic'
    ACTIVITY = 'activity'
    LOYALTY = 'loyalty'
    OTHER = 'other'
    DYNAMIC = 'dynamic'


class DynamicFieldStatus:
    ENABLE = 1
    DISABLE = 0
    DELETED = -1