#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class StoreCacheType:
    LOCAL = 1
    REDIS = 2


class ConsumerTopic:
    TOPIC_NOTIFY_SDK_RECEIVE_MESSAGE = "nm-sdk-receive-message"


class MobioEnvironment:
    KAFKA_BROKER = os.environ.get('KAFKA_BROKER')


