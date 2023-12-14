#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: locnh
    Company: MobioVN
    Date created: 27/05/2019
"""
from mobio.libs.kafka_lib.models.mongo.base_model import BaseModel


class RequeueConsumerModel(BaseModel):

    def __init__(self, client_mongo):
        super().__init__()
        self.client_mongo = client_mongo
        self.db_name = self.client_mongo.get_default_database().name
        self.collection = 'requeue_consumer'
