#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import requests
from mobio.libs.Singleton import Singleton
from mobio.sdks.admin import MobioAdminSDK

from .config import MobioEnvironment

logger = logging.getLogger()

@Singleton
class MerchantConfig:
    JWT_SECRET_KEY = 'jwt_secret_key'
    JWT_ALGORITHM = 'jwt_algorithm'
    BASIC_TOKEN = 'p_t'
    AUDIENCE_HOST = 'au_host'
    MEDIA_HOST = 'media_host'

    def __init__(self):
        self.configs = {}
        self.current_merchant = ''
        self.admin_host = None

    def set_adm_host(self, admin_host):
        self.admin_host = admin_host

    def get_merchant_config(self, merchant_id):
        if merchant_id not in self.configs:
            result = self.__request_get_merchant_auth(merchant_id)
            if result:
                self.configs[merchant_id] = result
        return self.configs[merchant_id]

    def __request_get_merchant_auth(self, merchant_id):
        merchant_config_host = MobioAdminSDK().request_get_merchant_config_host(
            merchant_id,
            key=None,
        )

        # media_host = result['data']['media_host']
        # if media_host.endswith('/'):
        #     media_host = media_host[:-1]
        return {
            "public_host": merchant_config_host["public-host"],
        }

    def set_current_merchant(self, merchant_id):
        self.get_merchant_config(merchant_id)
        if merchant_id != self.current_merchant:
            self.current_merchant = merchant_id

    def get_current_config(self):
        if not self.current_merchant:
            raise Exception("Please set merchant first")
        return self.configs[self.current_merchant]

    def get_current_token(self):
        if not self.current_merchant:
            raise Exception("Please set merchant first")
        configs = self.get_merchant_config(self.current_merchant)

        return configs[MerchantConfig.BASIC_TOKEN]

    def get_host_module_config(self, module_name):
        """
        :param module_name: Tên module cần lấy host
        : Khi lấy host của module thì kiểm tra hàm __request_get_merchant_auth đã set host vào kết quả trả về chưa
        :return:
        """

        if not self.current_merchant:
            raise Exception("Please set merchant first")
        configs = self.get_merchant_config(self.current_merchant)
        return configs[module_name]
