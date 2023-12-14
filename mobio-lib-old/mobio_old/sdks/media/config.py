#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Author: TungDD
    Company: MobioVN
    Date created: 03/06/2021

"""

import os


class Mobio:
    YEK_REWOP = os.environ.get('YEK_REWOP', '6ca79cc8-2636-4c1e-a5cd-ba135e28a902')
    MOBIO_TOKEN = 'Basic {}'.format(YEK_REWOP)


class SystemConfigKeys:
    JWT_SECRET_KEY = "jwt_secret_key"
    JWT_ALGORITHM = "jwt_algorithm"


class StoreCacheType:
    LOCAL = 1
    REDIS = 2


class ConsumerGroup:
    DEFAULT_MEDIA_GROUP = 'mobio-sdk-media-consumers'


class Application:
    APPLICATION_DATA_DIR = os.environ.get('APPLICATION_DATA_DIR')
    PUBLIC_DATA_DIR = os.environ.get('PUBLIC_DATA_DIR')


class ConsumerTopic:
    TOPIC_UPLOAD_MEDIA_SDK = 'upload_media_sdk'
    TOPIC_SAVE_INFO_MEDIA_SDK = 'save_info_media_sdk'
    TOPIC_OVERRIDE_MEDIA_SDK = 'override_media_sdk'
    TOPIC_DELETE_MEDIA_SDK = 'delete_media_sdk'


class Cache:
    PREFIX_KEY = "media_sdk_"


class MongoDB:
    MEDIA_MONGO_URI = os.environ.get('MEDIA_MONGO_URI')
    HOST_COLLECTION = "host"


class MobioEnvironment:
    HOST = os.environ.get('HOST')
    ADMIN_HOST = os.environ.get('ADMIN_HOST')
    REDIS_URI = os.environ.get('REDIS_URI')
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
    KAFKA_BROKER = os.environ.get('KAFKA_BROKER')
    KAFKA_REPLICATION_FACTOR = os.environ.get('KAFKA_REPLICATION_FACTOR')
    PUBLIC_HOST = os.environ.get('PUBLIC_HOST')

    YEK_REWOP = os.environ.get('YEK_REWOP', '6ca79cc8-2636-4c1e-a5cd-ba135e28a902')
    MOBIO_TOKEN = 'Basic {}'.format(YEK_REWOP)

    ADM_CONFIG = '{host}/adm/v1.0/merchants/{merchant_id}/configs'


class UrlConfig:
    GET_HOST_BY_MERCHANT = "{host}/media/{version}/merchants/actions/get-host"
