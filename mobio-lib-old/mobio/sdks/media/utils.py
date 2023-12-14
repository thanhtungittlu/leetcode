import os

import requests

from .config import MobioEnvironment, UrlConfig
from .merchant_config import MerchantConfig
from .mobio_media_sdk import MobioMediaSDK


@MobioMediaSDK.lru_cache.add()
def get_host_by_merchant_id(
        admin_host=None,
        merchant_id=None,
        request_timeout=None,
        media_api_version=None
):
    MerchantConfig().set_adm_host(admin_host)
    merchant_config = MerchantConfig().get_merchant_config(merchant_id)
    return merchant_config.get("public_host",
                               MobioEnvironment.PUBLIC_HOST) if merchant_config else MobioEnvironment.PUBLIC_HOST


def convert_bytes(num):
    if not num:
        return "0 bytes"
    if isinstance(num, str):
        return num
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_capacity(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size
    return None
