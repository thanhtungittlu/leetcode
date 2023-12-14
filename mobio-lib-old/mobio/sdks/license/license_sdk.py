from mobio.libs.Singleton import Singleton
from mobio.libs.caching import LruCache
from .config import StoreCacheType, Cache
from .crypt_utils import CryptUtil
from .utils import Utils

# from mobio.libs.ciphers import MobioCrypt2


def sdk_pre_check(func):
    def decorated_function(*args, **kwargs):
        if not MobioLicenseSDK().admin_host:
            raise ValueError("admin_host None")
        if not MobioLicenseSDK().lru_cache:
            raise ValueError("redis_uri None")
        if not MobioLicenseSDK().module_encrypt:
            raise ValueError("module_encrypt None")
        if not MobioLicenseSDK().module_use:
            raise ValueError("module_use None")
        if MobioLicenseSDK().admin_version not in MobioLicenseSDK.LIST_VERSION_VALID:
            raise ValueError("admin_version invalid")
        if not MobioLicenseSDK().module_valid:
            raise ValueError("module invalid")
        if not MobioLicenseSDK().license_key:
            raise ValueError("license_key none")
        return func(*args, **kwargs)

    return decorated_function


@Singleton
class MobioLicenseSDK(object):
    lru_cache = None
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 20
    LIST_VERSION_VALID = ["v1.0", "api/v2.0", "api/v2.1"]

    def __init__(self):
        self.admin_host = ""
        self.admin_version = MobioLicenseSDK.LIST_VERSION_VALID[-1]
        self.module_encrypt = ""
        self.module_use = ""
        self.request_header = None
        self.module_valid = False
        self.redis_uri = None
        self.license_key = ""

    @property
    def p_module_valid(self):
        return self.module_valid

    def config(
        self,
        admin_host=None,
        redis_uri=None,
        module_use=None,
        module_encrypt=None,
        license_key=None,
    ):
        self.admin_host = admin_host
        self.module_encrypt = module_encrypt
        self.module_use = module_use
        self.license_key = license_key
        if module_use:
            self.request_header = {
                "X-Module-Request": module_use,
                "X-Mobio-SDK": "LICENSE",
            }
        if module_use and module_encrypt:
            # if module_use == MobioCrypt2.d1(module_encrypt, enc="utf-8"):
            #     self.module_valid = True
            # else:
            #     self.module_valid = False
            self.module_valid = True
        if redis_uri:
            self.redis_uri = redis_uri
            MobioLicenseSDK.lru_cache = LruCache(
                store_type=StoreCacheType.REDIS,
                cache_prefix=Cache.PREFIX_KEY,
                redis_uri=redis_uri,
            )

    @sdk_pre_check
    def get_json_license(
        self,
        merchant_id,
    ):
        return CryptUtil.get_license_info(self.license_key, merchant_id)

    @sdk_pre_check
    def get_number_user(
        self,
        merchant_id,
    ):
        number_data = 0
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        if json_license:
            base_data = json_license.get("base_user", 0)
            if base_data < 0:
                return base_data
            else:
                if json_license.get("increase_user"):
                    number_data += json_license.get("increase_user", {}).get(
                        "total_user", 0
                    )
                if json_license.get("gift_user"):
                    number_data += json_license.get("gift_user", 0)
                number_data += base_data
        return {"number": number_data}

    @sdk_pre_check
    def get_number_profile(
        self,
        merchant_id,
    ):
        number_data = 0
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        if json_license:
            base_data = json_license.get("base_profile", 0)
            if base_data < 0:
                return base_data
            else:
                if json_license.get("gift_profile"):
                    base_data += json_license.get("gift_profile", 0)
                number_data += base_data
        return {"number": number_data}

    @sdk_pre_check
    def get_number_profile_anonymous(
        self,
        merchant_id,
    ):
        number_data = 0
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        if json_license:
            base_data = json_license.get("base_anynomous_profile", 0)
            if base_data < 0:
                return base_data
            else:
                if json_license.get("gift_anynomous_profile"):
                    base_data += json_license.get("gift_anynomous_profile", 0)
                number_data += base_data
        return {"number": number_data}

    @sdk_pre_check
    def get_number_page_social(
        self,
        merchant_id,
    ):
        number_data = 0
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        if json_license:
            social_chat = json_license.get("social_chat", {})
            if social_chat.get("allow", 0) == 1:
                base_data = social_chat.get("page_social", 0)
                if base_data < 0:
                    return base_data
                else:
                    if json_license.get("gift_page_social"):
                        base_data += json_license.get("gift_page_social", 0)
                    number_data += base_data
        return {"number": number_data}

    @sdk_pre_check
    def get_number_messages_allow_used(self, merchant_id, day_of_month=None):
        number_mess, messages = Utils.calculator_number_mess_allow_used(
            self.license_key, merchant_id, day_of_month=day_of_month
        )
        return {"number": number_mess, "messages": messages}

    @sdk_pre_check
    def use_message_for_campaign(
        self, merchant_id, number_of_message=None, day_of_month=None
    ):
        number_mess, messages, allow_use_mess = Utils.create_number_mess_need_used(
            self.license_key,
            merchant_id,
            number_mess_need_used=number_of_message,
            day_of_month=day_of_month,
        )
        return {
            "number": number_mess,
            "messages": messages,
            "success": allow_use_mess,
        }

    @staticmethod
    def encrypt2(data: str):
        return CryptUtil.encrypt_mobio_crypt2(data)

    @staticmethod
    def decrypt2(data: str):
        return CryptUtil.decrypt_mobio_crypt2(data)

    @staticmethod
    def decrypt1(key_salt: str, data: str):
        return CryptUtil.decrypt_mobio_crypt1(key_salt, data)

    @sdk_pre_check
    def merchant_has_expired(self, merchant_id):
        return Utils.check_merchant_expire(self.license_key, merchant_id)


