import os
import re
from copy import deepcopy


class StoreCacheType:
    LOCAL = 1
    REDIS = 2


class Cache:
    PREFIX_KEY = "license_sdk_"


class ConfigKeyHost:
    PROFILING_HOST = "profiling_host"
    PROFILING_IS_ONPREMISE = "profiling_is_onpremise"
    PROFILING_ONPREMISE_HOST = "profiling_onpremise_host"

    ON_PREMISE_TOKEN = "p_t"

    SOCIAL_HOST = "social_host"
    SOCIAL_IS_ONPREMISE = "social_is_onpremise"
    SOCIAL_ONPREMISE_HOST = "social_onpremise_host"

    CALLCENTER_IS_ONPREMISE = "callcenter_is_onpremise"
    CALLCENTER_HOST = "callcenter_host"

    NM_HOST = "nm_host"
    VOUCHER_HOST = "voucher_host"

    DNC_HOST = "dnc_host"
    DNC_IS_ONPREMISE = "dnc_is_onpremise"
    DNC_ONPREMISE_HOST = "dnc_onpremise_host"


class UrlConfig:
    ADMIN_CONFIG = "{host}/adm/{version}/merchants/{merchant_id}/configs"
    PARTNER_INFO = "{host}/adm/{version}/partners/{partner_id}/info"
    PARTNER_INFO_CIPHER_ENCRYPT = (
        "{host}/adm/{version}/partners/{partner_id}/info/encrypt"
    )
    ADMIN_GET_FILE_LICENSE = "{host}/adm/{version}/download-license"
    LICENSE_DOWNLOAD_FILE = "{host}/license/api/v1.0/license-merchant/download"
    ADMIN_MERCHANT_PARENT = "{host}/adm/{version}/merchants/{merchant_id}/parent"

class Mongo:
    ADMIN_MONGO_DB = os.environ.get(
        "ADMIN_MONGO_URI",
        "mongodb://administrationuser:5FfYiI_D7xw^h@api-test1.mobio.vn:27018/administration",
    )
    admin_mongo_db_name = re.search(
        r"^mongodb://[^@]+@[^/]+/([^?$]+).*$", ADMIN_MONGO_DB
    ).group(1)
    ADMIN_MONGO_DB_DB_NAME = deepcopy(str(admin_mongo_db_name))


class PathDir:
    APPLICATION_DATA_DIR = os.environ.get("APPLICATION_DATA_DIR")
    LICENSE_FOLDER_NAME = "License"
    PATH_DIR_LICENSE_FILE = APPLICATION_DATA_DIR + LICENSE_FOLDER_NAME + "/file_license"


class Mobio:
    vm_type = os.environ.get("VM_TYPE")
    YEK_REWOP = os.environ.get("YEK_REWOP", "f38b67fa-22f3-4680-9d01-c36b23bd0cad")
    MOBIO_TOKEN = "Basic {}".format(YEK_REWOP)
    AUTO_RENEW_FILE_LICENSE = os.environ.get("AUTO_RENEW_LICENSE")
