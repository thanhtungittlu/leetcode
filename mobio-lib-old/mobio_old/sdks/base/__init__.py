#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask


class MobioApplication(Flask):
    def __init__(self, args, **kwargs):
        super().__init__(args, **kwargs)
        pass
