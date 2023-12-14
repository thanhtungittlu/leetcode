#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ParamMessage:
    SOURCE = "source"
    MERCHANT_ID = "merchant_id"
    MESSAGE_TYPE = "message_type"
    KEY_CONFIG = "key_config"
    ACCOUNT_IDS = "account_ids"
    DATA_KWARGS = "data_kwargs"
    LIST_FIELD_REQUIRED = [MERCHANT_ID, KEY_CONFIG]


class MessageTypeValue:
    SEND_ALL = "send_all"
    SEND_SOCKET = "send_socket"
    SEND_EMAIL = "send_email"
    SEND_PUSH_ID_MOBILE_APP = "send_push_id_mobile_app"

