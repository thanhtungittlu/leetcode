#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
               ..
              ( '`<
               )(
        ( ----'  '.
        (         ;
         (_______,' 
    ~^~^~^~^~^~^~^~^~^~^~
    Author: thong
    Company: M O B I O
    Date Created: 14/03/2023
"""


class DataAdapter:

    def build_query(self, _filter):
        raise NotImplementedError()

    def execute_query(self, _query):
        raise NotImplementedError()
