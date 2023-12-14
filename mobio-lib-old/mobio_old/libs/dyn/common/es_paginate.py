#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 31/08/2018
"""
import json

from mobio.libs.dyn.common.utils import Base64


class ESPaginate(object):
    @staticmethod
    def generate_after_token(item):
        """
        Hàm dùng để generate token cho page tiếp theo. (dùng cho elaticsearch)
        Sử dụng cơ chế search_after của Elaticsearch. Để generate được token của cho page tiếp theo, item phải có thuộc
        tính _sort(do list danh sách của page trước được sắp xếp).
        :param item: item cuối cùng của page trước.
        :return: token: giá trị dùng để client request lấy page tiếp theo.
        """
        if hasattr(item, '_sort'):
            return Base64.encode(json.dumps(item._sort, ensure_ascii=False))
        elif not (isinstance(item, dict) and not item.get('sort')):
            return Base64.encode(json.dumps(item['sort'], ensure_ascii=False))

        print(
            'es_paginate::generate_after_token():item has not support paging. item must has _sort in property '
            'or sort in dict')
        return ''

    @staticmethod
    def parse_token(token):
        if not token:
            return None

        must_condition = json.loads(Base64.decode(token))
        print('es_paginate::parse_token():must_condition: %s' % must_condition)
        return must_condition
