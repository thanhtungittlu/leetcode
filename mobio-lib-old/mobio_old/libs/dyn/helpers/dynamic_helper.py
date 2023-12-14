#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: locnh
    Company: MobioVN
    Date created: 01/06/2019
"""
import configparser
from mobio.libs.dyn.common import Elastic
from mobio.libs.dyn.helpers.field_validate import FieldValidate
from mobio.libs.dyn.models.elastic.base_model import ElasticSearchBaseModel


class DynamicHelper:
    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_name, 'utf-8')
        try:
            if self.config.has_section(Elastic.__name__):
                if self.config.get(Elastic.__name__, Elastic.INDEX):
                    self.index = self.config.get(Elastic.__name__, Elastic.INDEX)
        except:
            pass

    def add_els_config(self, index):
        self.index = index

    def create_elastic_mapping(self, arr_fields):
        """
        Create elasticsearch mapping json base on field property for dynamic field.
        :param arr_fields: list dynamic fields
        :return: elasticsearch mapping string
        """
        try:
            r = {}
            for field in arr_fields:

                field_validate = FieldValidate(field, -1)
                r.update(field_validate.create_elastic_mapping())

            es = ElasticSearchBaseModel().get_elasticsearch()

            if es.indices.exists(index=self.index):
                result = es.indices.put_mapping(
                    index=self.index,
                    # doc_type=self.doc_type,
                    body={"properties": r}
                )
                return result
            else:
                print('DynamicHelper::create_elastic_mapping: index %s in elasticsearch not exists' % self.index)
                return False
        except Exception as e:
            print('DynamicHelper::create_elastic_mapping: exception: %s' % e)
            raise e
