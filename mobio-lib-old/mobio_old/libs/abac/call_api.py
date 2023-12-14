import requests

from .config import lru_redis_cache, Mobio


class APIRequest:
    TimeOut = 10
    ADMIN_GET_FULL_INFO_ACCOUNT = "{domain}/adm/api/v2.1/accounts/{account_id}/full-info"
    ADMIN_GET_LIST_ACTION_FOR_MERCHANT = "{domain}/adm/api/v2.1/policies/actions/sdk"
    ADMIN_GET_LIST_STATEMENT = "{domain}/adm/api/v2.1/statements"


_TIME_CACHE = 900 if Mobio.VM_TYPE and Mobio.VM_TYPE != "TEST" else 60
# _TIME_CACHE = 60


class CallAPI:

    # TODO: thay expiration cho production
    @staticmethod
    @lru_redis_cache.add(expiration=_TIME_CACHE)
    def admin_get_account_info(merchant_id, account_id):
        # try:
        url = APIRequest.ADMIN_GET_FULL_INFO_ACCOUNT.format(domain=Mobio.ADMIN_HOST, account_id=account_id)
        authorization = Mobio.MOBIO_TOKEN
        data_res = requests.get(
            url,
            headers={
                "Authorization": authorization,
                "X-Merchant-ID": merchant_id,
            },
            timeout=APIRequest.TimeOut,
        )
        data = None
        if data_res.status_code == 200:
            if data_res.json().get("data"):
                data = data_res.json().get("data")
        # print("abac_sdk admin_get_account_info: {}".format(data))
        return data
        # except Exception as er:
        #     err_msg = "abac_sdk admin_get_account_info err: {}".format(er)
        #     print(err_msg)
        #     return {}

    @lru_redis_cache.add()
    @staticmethod
    def admin_get_json_action(merchant_id):
        # try:
        url = APIRequest.ADMIN_GET_LIST_ACTION_FOR_MERCHANT.format(domain=Mobio.ADMIN_HOST)
        authorization = Mobio.MOBIO_TOKEN
        data_res = requests.get(
            url,
            headers={
                "Authorization": authorization,
                "X-Merchant-ID": merchant_id,
            },
            timeout=APIRequest.TimeOut,
            params={"page": "-1"}
        )
        data = {}
        if data_res.status_code == 200:
            if data_res.json().get("data"):
                list_data = data_res.json().get("data")
                for i in list_data:
                    data[i.get("resource") + ":" + i.get("key")] = i
        # print("abac_sdk admin_get_json_action: {}".format(data))
        return data
        # except Exception as er:
        #     err_msg = "abac_sdk admin_get_json_action err: {}".format(er)
        #     print(err_msg)
        #     return {}

    # TODO: thay expiration cho production
    @staticmethod
    @lru_redis_cache.add(expiration=_TIME_CACHE)
    def admin_get_list_statement(merchant_id, account_id, resource, action, service):
        """
        :param merchant_id:
        :param account_id:
        :param resource:
        :param action:
        :return: [{
            "effect": "allow",
            "action": [
                "DealViewReport"
            ],
            "resource": [
                "sale:deal"
            ],
            "condition": [
                {
                    "operator": "StringEquals",
                    "field": "user:block",
                    "values": [
                        "KHDN"
                    ],
                    "qualifier": "ForAnyValue",
                    "if_exists": False,
                    "ignore_case": False
                },
                {
                    "operator": "StringEquals",
                    "field": "deal:block",
                    "values": [
                        "${user:block}"
                    ],
                    "qualifier": "ForAnyValue",
                    "if_exists": False,
                    "ignore_case": False
                },
                {
                    "operator": "StringStartsWith",
                    "field": "deal:scope_code",
                    "values": [
                        "${user:scope_code}"
                    ],
                    "qualifier": "ForAnyValue",
                    "if_exists": False,
                    "ignore_case": False
                }
            ]
        }]
        """
        # try:
        url = APIRequest.ADMIN_GET_LIST_STATEMENT.format(domain=Mobio.ADMIN_HOST)
        authorization = Mobio.MOBIO_TOKEN
        body_req = {
            'user_ids': [account_id],
            'team_ids': [],
            'merchant_ids': [merchant_id],
            'resources': service + ":" + resource,
            'actions': resource + ":" + action
        }
        data_res = requests.post(
            url,
            json=body_req,
            headers={
                "Authorization": authorization,
                "X-Merchant-ID": merchant_id,
            },
            timeout=APIRequest.TimeOut,
        )
        data = None
        if data_res.status_code == 200:
            if data_res.json().get("statements"):
                data = data_res.json().get("statements")
        # TODO: comment log khi len prod
        # print("abac_sdk admin_get_list_statement: {}".format(data))
        return data

        # return [
        #     {
        #         "effect": "allow",
        #         "action": [
        #             "ListFromSale"
        #         ],
        #         "resource": [
        #             "sale:deal"
        #         ],
        #         "condition": [
        #             {
        #                 "operator": "StringEquals",
        #                 "field": "deal:block",
        #                 "values": [
        #                     "${user:block}"
        #                 ],
        #                 "qualifier": "ForAnyValue",
        #                 "if_exists": False,
        #                 "ignore_case": False
        #             },
        #             {
        #                 "operator": "StringStartsWith",
        #                 "field": "deal:scope_code",
        #                 "values": [
        #                     "${user:scope_code}"
        #                 ],
        #                 "qualifier": "ForAnyValue",
        #                 "if_exists": False,
        #                 "ignore_case": False
        #             }
        #         ]
        #     },
        #             {
        #                 "effect": "allow",
        #                 "action": [
        #                     "ListFromSale"
        #                 ],
        #                 "resource": [
        #                     "sale:deal"
        #                 ],
        #                 "condition": [
        #                     {
        #                         "operator": "StringStartsWith",
        #                         "field": "deal:scope_code",
        #                         "values": [
        #                             "3#7", "3#8", "3#9"
        #                         ],
        #                         "qualifier": "ForAnyValue",
        #                         "if_exists": False,
        #                         "ignore_case": False
        #                     },
        #                     {
        #                         "operator": "StringEquals",
        #                         "field": "user:scope_code",
        #                         "values": [
        #                             "3#6"
        #                         ],
        #                         "qualifier": "ForAnyValue",
        #                         "if_exists": False,
        #                         "ignore_case": False
        #                     }
        #                 ]
        #             }
        # ]

        # except Exception as er:
        #     err_msg = "abac_sdk admin_get_list_statement err: {}".format(er)
        #     print(err_msg)
        #     return []
