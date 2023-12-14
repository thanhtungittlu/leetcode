#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: AnhNT
    Company: MobioVN
    Date created: 2021/06/03
"""

import hashlib
import json
from Crypto.Cipher import AES
from .config import PathDir, UrlConfig, Mobio
import time
import os
import base64
import numpy as np
import requests
from mobio.libs.Singleton import Singleton
from mobio.libs.caching import LRUCacheDict
from pathlib import Path


class MobioCrypt1:
    @staticmethod
    def _g(pd, s):
        n1 = 0x407
        m1 = [0x73, 0x68, 0x61]
        m2 = [0x35, 0x31, 0x32]
        m = "".join([chr(i) for i in m1]) + "".join([chr(i) for i in m2])
        dk = hashlib.pbkdf2_hmac(m, pd.encode(), s, n1).hex()
        return dk[:0x20]

    @staticmethod
    def __u(s):
        return s[: -ord(s[len(s) - 1 :])]

    @staticmethod
    def d1(enc, password, salt):
        p = MobioCrypt1._g(password, salt)
        i = enc[:0x10]
        cer = AES.new(bytes(p, "utf-8"), AES.MODE_CBC, i)
        return MobioCrypt1.__u(cer.decrypt(enc[0x10:])).decode("utf8")

    @staticmethod
    def g1(p, t, s):
        if s != 0x1341589:
            return ""
        if t == 1:
            return (
                hashlib.md5(bytes(p, "utf-8")).hexdigest()
                + hashlib.md5(bytes(p, "utf-8")).hexdigest()
            )
        if t == 2:
            ps = p.split("-")
            if len(ps) == 4:
                return ""
            return ps[1] + ps[3]


class MobioCrypt2:
    @staticmethod
    def __f1(x1):
        x = v = 1
        y = u = 0
        a = 0x100
        b = x1 % 0x100
        while b != 0:
            q = int(a / b)
            r = int(a - b * q)
            s = int(x - u * q)
            t = int(y - v * q)
            a = b
            x = u
            y = v
            b = r
            u = s
            v = t
        while y < 0:
            y += 0x100
        while y > 0x100:
            y -= 0x100
        return y

    @staticmethod
    def __f2():
        return np.random.randint(1, 0x100, 0x0A)

    @staticmethod
    def e1(raw):
        if isinstance(raw, str):
            raw = raw.encode("utf-8")

        ln = len(raw)

        r1 = bytearray()
        tmp = MobioCrypt2.__f2()

        for i in range(0, len(tmp)):
            r1.append(tmp[i])

        i = r1[0]
        k = r1[1]

        i += 1 if i % 2 == 0 else 0
        i = 0x8F if i == 1 else i

        for j in range(0, ln):
            tmp = (int(raw[j]) * i + k + r1[(2 + (j % 8))]) % 0x100
            while tmp >= 0x100:
                tmp -= 0x100
            while tmp < 0:
                tmp += 0x100
            r1.append(tmp)
        r1 = MobioCrypt3.e1(r1).rstrip("=")
        return r1 + hashlib.md5(r1.encode("utf-8")).hexdigest()

    @staticmethod
    def d1(encrypted, enc=None):
        raw = encrypted[0 : len(encrypted) - 0x20]
        c1 = encrypted[len(encrypted) - 0x20 :]
        c2 = hashlib.md5(raw.encode("utf-8")).hexdigest()
        if c2 != c1:
            return None

        raw = MobioCrypt3.d1(raw)
        ln = len(raw)

        i = raw[0]
        i += 1 if i % 2 == 0 else 0
        i = 0x8F if i == 1 else i

        lc = MobioCrypt2.__f1(i)
        m = raw[1]
        r1 = bytearray()
        for j in range(10, ln):
            tmp = ((int(raw[j]) - raw[(2 + ((j - int(0x0A)) % 8))] - m) * lc) % 0x100
            while tmp >= 0x100:
                tmp -= 0x100
            while tmp < 0:
                tmp += 0x100
            if j >= 10:
                r1.append(tmp)
        if enc:
            return r1.decode(encoding=enc)
        return r1


class MobioCrypt3:
    @staticmethod
    def e1(raw):
        try:
            bs = raw
            if isinstance(raw, str):
                bs = raw.encode("utf-8")

            ed = base64.b64encode(bs)
            return ed.decode(encoding="UTF-8")
        except:
            return ""

    @staticmethod
    def e2(raw):
        return MobioCrypt3.e1(raw).rstrip("=")

    @staticmethod
    def d1(raw, enc=None):
        try:
            if isinstance(raw, bytes):
                raw = raw.decode("UTF-8")
            dd = base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4))
            if enc:
                return dd.decode(encoding=enc)
            return dd
        except:
            return None


@Singleton
class CryptUtil:
    def __init__(self):
        self.license_merchant = LRUCacheDict(expiration=900)

    @staticmethod
    def decrypt_mobio_crypt1(key_salt, text_encrypt):
        m = MobioCrypt1.g1(key_salt, 1, 0x1341589)
        u = MobioCrypt1.g1(key_salt, 2, 0x1341589)
        return MobioCrypt1.d1(bytes.fromhex(text_encrypt), m, bytes(u, "utf-8"))

    @staticmethod
    def get_file_path_license(merchant_id):
        license_file_name = hashlib.md5(bytes(merchant_id, "utf-8")).hexdigest()
        file_path = "{}/{}.{}".format(
            PathDir.PATH_DIR_LICENSE_FILE, license_file_name, "license"
        )
        print("license_sdk::file path: {}".format(file_path))
        return file_path

    @staticmethod
    def get_content_from_file(file_path):
        content_file = None
        if not os.path.exists(file_path):
            return content_file
        i = 0
        while True:
            try:
                if i >= 10:
                    break
                with open(file_path, "r") as fout:
                    content_file = fout.read()
                    fout.close()
                break
            except IOError as ex:
                print("license_sdk::get_content_from_file():message: %s" % ex)
                time.sleep(0.1)
                i += 1
        print("license_sdk::content file license: {}".format(content_file))
        return content_file

    @staticmethod
    def save_data_to_file(file_path, data):
        i = 0
        while True:
            try:
                if i >= 10:
                    break
                Path(os.path.dirname(os.path.abspath(file_path))).mkdir(
                    parents=True, exist_ok=True
                )
                with open(file_path, "w") as fout:
                    fout.write(data)
                    fout.close()
                print("license_sdk::save_data_to_file success")
                break
            except IOError as ex:
                print("license_sdk::save_data_to_file():message: %s" % ex)
                time.sleep(0.1)
                i += 1

    @staticmethod
    def get_license_info(license_key, merchant_id):
        license_info = None
        try:
            from .call_api import get_parent_id_from_merchant
            print("license_sdk:: get_license_info merchant_id: {}".format(merchant_id))
            root_merchant_id = get_parent_id_from_merchant(merchant_id)
            print("license_sdk:: get_license_info root_merchant_id: {}".format(root_merchant_id))
            license_encrypt = CryptUtil.get_license_encrypt(root_merchant_id)
            private_key = license_key + merchant_id
            m = MobioCrypt1.g1(private_key, 1, 0x1341589)
            u = MobioCrypt1.g1(private_key, 2, 0x1341589)
            json_body = json.loads(
                MobioCrypt1.d1(bytes.fromhex(license_encrypt), m, bytes(u, "utf-8")),
                encoding="utf-8",
            )
            u1 = u
            u1 += str(json_body.get("t01")) + str(json_body.get("t06"))
            license_info = json.loads(
                MobioCrypt1.d1(
                    bytes.fromhex(json_body.get("data")), m, bytes(u1, "utf-8")
                ),
                encoding="utf-8",
            )
        except Exception as ex:
            print("license_sdk::get_license_info():message: {}".format(ex))
        return license_info

    @staticmethod
    def check_key_valid_function(key_valid, func_name):
        invalid = False
        try:
            text_decrypt = MobioCrypt2.d1(key_valid, "utf-8")
            list_param = text_decrypt.split("_")
            if len(list_param) >= 3:
                if list_param[0] == func_name:
                    if list_param[1] == "dev":
                        time_expire = int(list_param[2])
                        if time_expire > time.time():
                            invalid = True
                    elif list_param[1] == "prod":
                        invalid = True
        except Exception as ex:
            print("license_sdk::check_key_valid_function():message: {}".format(ex))
        return invalid

    @staticmethod
    def get_file_license_from_admin(merchant_id):
        from .license_sdk import MobioLicenseSDK

        license_encrypt = ""
        try:
            adm_url = str(UrlConfig.ADMIN_GET_FILE_LICENSE).format(
                host=MobioLicenseSDK().admin_host,
                version=MobioLicenseSDK().admin_version,
            )
            request_header = {"Authorization": Mobio.MOBIO_TOKEN}
            if MobioLicenseSDK().request_header:
                request_header.update(MobioLicenseSDK().request_header)
            params = {"merchant_id": merchant_id}
            response = requests.get(
                adm_url,
                params=params,
                headers=request_header,
                timeout=MobioLicenseSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            license_encrypt = response.text
        except Exception as ex:
            print("license_sdk::get_file_license_from_admin():message: {}".format(ex))
        print(
            "license_sdk::get_file_license_from_admin license_encrypt: {}".format(
                license_encrypt
            )
        )
        return license_encrypt

    @staticmethod
    def get_license_encrypt(merchant_id):
        license_encrypt = ""
        try:
            try:
                license_encrypt = CryptUtil().license_merchant.getitem(merchant_id)
            except Exception as ex:
                print(
                    "license_sdk::get_license_encrypt():get cache none for key: {}".format(
                        ex
                    )
                )
            print("license_sdk::license_encrypt cache: {}".format(license_encrypt))
            if not license_encrypt:
                print("license_sdk::license_encrypt no cache")
                if Mobio.vm_type:
                    print("license_sdk::server get license")
                    if (
                        Mobio.AUTO_RENEW_FILE_LICENSE
                        and Mobio.AUTO_RENEW_FILE_LICENSE == "yes"
                    ):
                        print("license_sdk::renew file license")
                        license_encrypt = CryptUtil.get_file_license_from_license(
                            merchant_id
                        )
                        if license_encrypt:
                            print("license_sdk::renew success")
                            file_path = CryptUtil.get_file_path_license(merchant_id)
                            CryptUtil.save_data_to_file(file_path, license_encrypt)
                    if not license_encrypt:
                        print("license_sdk::get content file license")
                        file_path = CryptUtil.get_file_path_license(merchant_id)
                        license_encrypt = CryptUtil.get_content_from_file(file_path)
                else:
                    print("license_sdk::local get file license")
                    license_encrypt = CryptUtil.get_file_license_from_admin(merchant_id)
                if license_encrypt:
                    print("license_sdk::save cache file license")
                    CryptUtil().license_merchant.set_item(merchant_id, license_encrypt)
        except Exception as ex:
            print("license_sdk::get_license_encrypt():message: {}".format(ex))
        return license_encrypt

    @staticmethod
    def get_file_license_from_license(merchant_id):
        from .license_sdk import MobioLicenseSDK

        license_encrypt = ""
        try:
            adm_url = str(UrlConfig.LICENSE_DOWNLOAD_FILE).format(
                host=MobioLicenseSDK().admin_host,
            )
            request_header = {}
            if MobioLicenseSDK().request_header:
                request_header.update(MobioLicenseSDK().request_header)
            params = {"merchant_id": merchant_id}
            response = requests.get(
                adm_url,
                params=params,
                headers=request_header,
                timeout=MobioLicenseSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            license_encrypt = response.text
        except Exception as ex:
            print("license_sdk::get_file_license_from_license():message: {}".format(ex))
        print(
            "license_sdk::get_file_license_from_license license_encrypt: {}".format(
                license_encrypt
            )
        )
        return license_encrypt

    @staticmethod
    def encrypt_mobio_crypt2(data: str):
        return MobioCrypt2.e1(data)

    @staticmethod
    def decrypt_mobio_crypt2(data: str):
        return MobioCrypt2.d1(data, "utf-8")

