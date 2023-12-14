#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: locnh
    Company: MobioVN
    Date created: 30/05/2019
"""
from datetime import datetime

import unidecode
from mobio.libs.dyn.models.mongo import DynamicFieldStructure, DynamicFieldProperty, DisplayType
from mobio.libs.dyn.models.mongo.merchant_config import DATE_PICKER_FORMAT


class UnSupportedDynamicField(Exception):
    pass


DISPLAY_TYPE_IS_LIST_TYPE = [DisplayType.MULTI_LINE.value, DisplayType.DROPDOWN_MULTI_LINE.value, DisplayType.CHECKBOX.value, DisplayType.TAGS.value]


class FieldValidate(object):
    # def __init__(self, field_property, field_key, display_type, field_value):
    #     self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY) = field_key
    #     self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) = field_property
    #     self.display_type = display_type
    #     self.field_value = field_value

    def __init__(self, dynamic_field, field_value):
        self.dynamic_field = dynamic_field
        self.field_value = field_value

    def datetime_parser(self, str_datetime):
        date_value = None
        lst_format = ['%d/%m', '%d-%m', '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%Y %H:%M', '%d-%m-%Y %H:%M', '%d/%m/%Y %H:%M:%S', '%d-%m-%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.000Z']
        for f in lst_format:
            try:
                date_value = datetime.strptime(str_datetime, f)
                if date_value:
                    break
            except Exception as ex:
                print('datetime_parser: parse: {}, ex: {}'.format(str_datetime, ex))
        return date_value

    def norm_value(self):
        if self.field_value is None:
            return self.field_value

        if self.dynamic_field is None:
            print('FieldValidate::norm_value: dynamic_field is NONE')
            return None

        if self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.INTEGER:
            if self.dynamic_field.get(DynamicFieldStructure.DISPLAY_TYPE) in DISPLAY_TYPE_IS_LIST_TYPE:
                if type(self.field_value) is str:
                    arr_data = self.field_value.split(';')
                    lst_data = []
                    for data in arr_data:
                        try:
                            data = int(data)
                            lst_data.append(data)
                        except ValueError as ex:
                            print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                    if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                        lst_data = [x for x in lst_data if str(x).strip() in [str(y.get('name')) for y in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)]]
                    return lst_data
                elif type(self.field_value) is list:
                    try:
                        lst_data = [int(x) for x in self.field_value]
                        if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                            lst_data = [x for x in lst_data if str(x).strip() in [str(y.get('name')) for y in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)]]
                        return lst_data
                    except ValueError as ex:
                        print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                        return None
                else:
                    try:
                        lst_data = [int(self.field_value)]
                        if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                            lst_data = [x for x in lst_data if str(x).strip() in [str(y.get('name')) for y in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)]]
                        return lst_data
                    except ValueError as ex:
                        print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                        return None
            else:
                try:
                    data = int(self.field_value)
                    if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                        data = next((int(x.get('name')) for x in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) if str(x.get('name')) == str(data)), None)
                    return data
                except ValueError as ex:
                    print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                    return None
        elif self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.STRING:
            if self.dynamic_field.get(DynamicFieldStructure.DISPLAY_TYPE) in DISPLAY_TYPE_IS_LIST_TYPE:
                if type(self.field_value) is str:
                    arr_data = self.field_value.split(';')
                    lst_data = []
                    for data in arr_data:
                        try:
                            data = str(data)
                            lst_data.append(data)
                        except ValueError as ex:
                            print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                    if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                        lst_data = [x for x in lst_data if str(x).strip() in [str(y.get('name')) for y in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)]]
                    return lst_data
                elif type(self.field_value) is list:
                    lst_data = [str(x) for x in self.field_value]
                    if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                        lst_data = [x for x in lst_data if str(x).strip() in [str(y.get('name')) for y in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)]]
                    return lst_data
                else:
                    try:
                        lst_data = [str(self.field_value)]
                        if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                            lst_data = [x for x in lst_data if str(x).strip() in [str(y.get('name')) for y in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)]]
                        return lst_data
                    except ValueError as ex:
                        print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                        return None
            else:
                try:
                    data = str(self.field_value)
                    if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                        data = next((x.get('name') for x in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) if str(x.get('name')) == str(data)), None)
                    return data
                except ValueError as ex:
                    print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                    return None
        elif self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.FLOAT:
            if self.dynamic_field.get(DynamicFieldStructure.DISPLAY_TYPE) in DISPLAY_TYPE_IS_LIST_TYPE:
                if type(self.field_value) is str:
                    arr_data = self.field_value.split(';')
                    lst_data = []
                    for data in arr_data:
                        try:
                            data = float(data)
                            lst_data.append(data)
                        except ValueError as ex:
                            print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                    if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                        lst_data = [x for x in lst_data if str(x).strip() in [str(y.get('name')) for y in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)]]
                    return lst_data
                elif type(self.field_value) is list:
                    try:
                        lst_data = [float(x) for x in self.field_value]
                        if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                            lst_data = [x for x in lst_data if str(x).strip() in [str(y.get('name')) for y in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)]]
                        return lst_data
                    except ValueError as ex:
                        print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                        return None
                else:
                    try:
                        lst_data = [float(self.field_value)]
                        if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                            lst_data = [x for x in lst_data if str(x).strip() in [str(y.get('name')) for y in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)]]
                        return lst_data
                    except ValueError as ex:
                        print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                        return None
            else:
                try:
                    data = float(self.field_value)
                    if self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) and len(self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED)) > 0:
                        data = next((float(x.get('name')) for x in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) if str(x.get('name')) == str(data)), None)
                    return data
                except ValueError as ex:
                    print('field_validate::norm_value: parse: {}, ex: {}'.format(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY), ex))
                    return None
        elif self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.DATETIME:
            date_format = next((x for x in DATE_PICKER_FORMAT if self.dynamic_field.get(DynamicFieldStructure.FORMAT) == x.get('key')), None)
            if date_format:
                value = self.datetime_parser(str(self.field_value)) if type(self.field_value) != datetime else self.field_value
                if value is None:
                    return None
                if date_format.get('year'):
                    value = value.replace(year=date_format.get('year'))
                return value
            else:
                return None
        elif self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.UDT:
            if type(self.field_value) == int:
                udt = next((x for x in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) if self.field_value == x.get('id')), None)
            elif type(self.field_value) == str:
                udt = next((x for x in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) if unidecode.unidecode(self.field_value.lower()) == unidecode.unidecode(x.get('name').lower())), None)
                if not udt:
                    udt = next((x for x in self.dynamic_field.get(DynamicFieldStructure.DATA_SELECTED) if str(self.field_value) == str(x.get('id'))), None)
            else:
                udt = None
            return udt.get('id') if udt else None
        else:
            return self.field_value

    def create_elastic_mapping(self):
        if self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) is None:
            print('FieldValidate::create_elastic_mapping: field property is None')
            return None

        if self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.INTEGER:
            return {
                self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY): {"type": "long"}
            }
        elif self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.FLOAT:
            return {
                self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY): {"type": "double"}
            }
        if self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.STRING:
            return {
                self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY): {"type": "keyword",
                                                                          "normalizer": "lowerasciinormalizer"}
            }
        if self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.DATETIME:
            return {
                self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY): {"type": "date"}
            }
        if self.dynamic_field.get(DynamicFieldStructure.FIELD_PROPERTY) == DynamicFieldProperty.UDT:
            return {
                self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY): {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "keyword", "normalizer": "lowerasciinormalizer"}
                    }
                }
            }
        raise UnSupportedDynamicField(self.dynamic_field.get(DynamicFieldStructure.FIELD_KEY))
