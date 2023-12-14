#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 20/04/2021
"""
from flask import Blueprint, jsonify

checking_service_mod = Blueprint('checking_service', __name__)


@checking_service_mod.route('/ping', methods=['GET'])
def ping():
    return jsonify({"code": 200}), 200
