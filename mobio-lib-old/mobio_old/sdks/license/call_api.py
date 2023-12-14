from .config import UrlConfig, Mobio
from .license_sdk import MobioLicenseSDK
import requests


@MobioLicenseSDK.lru_cache.add()
def get_parent_id_from_merchant(
        merchant_id
):
    api_version = MobioLicenseSDK().admin_version
    adm_url = str(UrlConfig.ADMIN_MERCHANT_PARENT).format(
        host=MobioLicenseSDK().admin_host,
        version=api_version,
        merchant_id=merchant_id,
    )
    request_header = {"Authorization": Mobio.MOBIO_TOKEN}
    if MobioLicenseSDK().request_header:
        request_header.update(MobioLicenseSDK().request_header)
    response = requests.get(
        adm_url,
        headers=request_header,
        timeout=MobioLicenseSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data_parent = response.json()
    if data_parent and data_parent.get("data") and len(data_parent.get("data")) > 0:
        root_merchant_id = data_parent.get("data")[0].get("root_merchant_id")
        if root_merchant_id:
            return root_merchant_id
    return merchant_id
