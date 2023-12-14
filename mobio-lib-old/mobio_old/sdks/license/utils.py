from .crypt_utils import CryptUtil
from .license_mess_used import LicenseMessUsedModel
from .license_detail_mess_used import LicenseDetailMessUsedModel
from copy import deepcopy
from .license_history_mess_used import LicenseHistoryMessUsedModel
from .date_utils import *


class Utils:
    DATE_YYYYmmdd = "%Y%m%d"
    DATE_YYYYmm = "%Y%m"
    TIME_ZONE = 420
    PERCENT_BASE = 50

    @staticmethod
    def license_get_value_by_key(license_key, merchant_id, key_get):
        json_license = CryptUtil.get_license_info(license_key, merchant_id)
        if json_license:
            return json_license.get(key_get)
        else:
            return None

    @staticmethod
    def get_data_mess_license(license_key, merchant_id):
        data_mess = {}
        json_license = CryptUtil.get_license_info(license_key, merchant_id)
        if json_license:
            data_mess["base_messages"] = json_license.get("base_messages", 0)
            data_mess["increase_messages"] = json_license.get("increase_messages", [])
            data_mess["gift_messages"] = json_license.get("gift_messages", [])
        return data_mess

    # lay so luong mess cho phep su dung trong license
    @staticmethod
    def get_mess_allow_in_license(data_mess, month_get_mess):
        list_block_mess_id, list_gift_code, data_number_mess = [], [], {}
        if data_mess.get("increase_messages"):
            for item in data_mess.get("increase_messages", []):
                try:
                    from_time = ConvertDateUTCtoStringITC(
                        convert_timestamp_to_date_utc(item.get("from_time")),
                        Utils.TIME_ZONE,
                        Utils.DATE_YYYYmm,
                    )
                    to_time = ConvertDateUTCtoStringITC(
                        convert_timestamp_to_date_utc(item.get("to_time")),
                        Utils.TIME_ZONE,
                        Utils.DATE_YYYYmm,
                    )
                    if month_get_mess >= from_time and month_get_mess <= to_time:
                        data_number_mess[item.get("block_mess_id")] = item.get(
                            "total_messages", 0
                        )
                        list_block_mess_id.append(item.get("block_mess_id"))
                except Exception as ex:
                    print(
                        "license_sdk::get_mess_allow_in_license():message: {}".format(
                            ex
                        )
                    )
                    continue
        if data_mess.get("gift_messages"):
            for item in data_mess.get("gift_messages", []):
                if item.get("type_use") == "one_times":
                    data_number_mess[item.get("gift_code")] = item.get("number", 0)
                    list_gift_code.append(item.get("gift_code"))
        print(
            "license_sdk::get_mess_allow_in_license list_block_mess_id: {}, list_gift_code: {}, data_number_mess: {}".format(
                list_block_mess_id, list_gift_code, data_number_mess
            )
        )
        return list_block_mess_id, list_gift_code, data_number_mess

    @staticmethod
    def get_time_using_mess(day_of_month):
        if day_of_month:
            last_month = convert_date_to_format(
                convert_str_to_date(day_of_month, Utils.DATE_YYYYmmdd).replace(day=1)
                - datetime.timedelta(days=1),
                Utils.DATE_YYYYmm,
            )
            month_get_mess = day_of_month[:6]
        else:
            dnow_itc = convert_date_utc_to_date_itc(get_utc_now(), Utils.TIME_ZONE)
            last_month = convert_date_to_format(
                dnow_itc.replace(day=1) - datetime.timedelta(days=1),
                Utils.DATE_YYYYmm,
            )
            month_get_mess = convert_date_to_format(dnow_itc, Utils.DATE_YYYYmm)
        print(
            "license_sdk::get_time_using_mess month_get_mess: {}, last_month: {}".format(
                month_get_mess, last_month
            )
        )
        return month_get_mess, last_month

    @staticmethod
    def calculator_number_mess_allow_used(license_key, merchant_id, day_of_month=None):
        number_mess, messages, allow_use_mess = Utils.create_number_mess_need_used(
            license_key,
            merchant_id,
            number_mess_need_used=None,
            day_of_month=day_of_month,
        )
        return number_mess, messages

    # kiem tra checksum du lieu co bi sua ko
    @staticmethod
    def check_data_mess_used(data_mess):
        data_invalid = False
        if not data_mess:
            return True
        try:
            check_sum = data_mess.get(LicenseMessUsedModel.check_sum)
            data_text = LicenseMessUsedModel().data_mess_to_string(data_mess)
            if CryptUtil.encrypt_mobio_crypt2(data_text) == check_sum:
                data_invalid = True
        except Exception as ex:
            print("license_sdk::check_data_mess_used():message: {}".format(ex))
        return data_invalid

    # kiem tra so luong mess trong license va so luong mess da su dung
    @staticmethod
    def get_number_remaining_messages(
        merchant_id, list_block_mess_id, list_gift_code, data_number_mess_license
    ):
        data_remaining_messages, total_mess = {}, 0
        list_mess_id = []
        if list_block_mess_id:
            list_mess_id.extend(list_block_mess_id)
        if list_gift_code:
            list_mess_id.extend(list_gift_code)
        data_used = LicenseDetailMessUsedModel().get_number_mess_used_from_mess_id(
            merchant_id, list_mess_id
        )
        list_id_remaining_block, list_id_remaining_gift = {}, {}
        total_mess_buy, total_mess_gift = 0, 0
        if data_number_mess_license:
            for key, value in data_number_mess_license.items():
                if key in list_block_mess_id:
                    total_mess_buy += value
                else:
                    total_mess_gift += value
                mess_used = value
                if data_used:
                    mess_used = value - data_used.get(key, 0)
                if mess_used > 0:
                    data_remaining_messages[key] = mess_used
                    total_mess += mess_used
                    if key in list_block_mess_id:
                        list_id_remaining_block[key] = value
                    else:
                        list_id_remaining_gift[key] = value
        data_remaining_messages["total_mess_buy"] = total_mess_buy
        data_remaining_messages["total_mess_gift"] = total_mess_gift
        print(
            "license_sdk::get_number_remaining_messages data_remaining_messages: {}, total_mess: {}".format(
                data_remaining_messages, total_mess
            )
        )
        print(
            "license_sdk::get_number_remaining_messages list_id_remaining_block: {}, list_id_remaining_gift: {}".format(
                list_id_remaining_block, list_id_remaining_gift
            )
        )
        return (
            data_remaining_messages,
            total_mess,
            list_id_remaining_block,
            list_id_remaining_gift,
        )

    # tinh toan su dung mess can gui
    @staticmethod
    def create_number_mess_need_used(
        license_key, child_merchant_id, number_mess_need_used=None, day_of_month=None
    ):
        number_mess, messages, allow_use_mess = 0, "", 0
        try:
            from .call_api import get_parent_id_from_merchant
            print("license_sdk:: create_number_mess_need_used merchant_id: {}".format(child_merchant_id))
            merchant_id = get_parent_id_from_merchant(child_merchant_id)
            print("license_sdk:: create_number_mess_need_used root_merchant_id: {}".format(merchant_id))
            # lấy thông tin mess trong file license
            data_mess_license = Utils.get_data_mess_license(license_key, merchant_id)
            if data_mess_license:
                base_messages_package = data_mess_license.get("base_messages", 0)
                # nếu base_messages < 0 nghĩa là gói enterprise ko giới hạn
                if base_messages_package < 0:
                    print(
                        "license_sdk::create_number_mess_need_used(): mess unlimit on package enterprise_package"
                    )
                    return -1, "enterprise_package_unlimited", 1
                # số mess dc sử dụng tăng thêm số base_messages
                number_mess += base_messages_package
                # lấy tháng trước và tháng hiện tại
                month_get_mess, last_month = Utils.get_time_using_mess(day_of_month)
                # từ thông tin license lọc ra khối mess thỏa mãn: tháng hiện tại có mess mua ko, có mess quà tặng ko
                (
                    list_block_mess_id,
                    list_gift_code,
                    data_number_mess_license,
                ) = Utils.get_mess_allow_in_license(data_mess_license, month_get_mess)

                # tính toán số mess đã sử dụng trc đó(quà tặng, mua thêm) để ra số lượng còn lại
                (
                    data_remaining_messages,
                    number_remaining_mess,
                    list_id_remaining_block,
                    list_id_remaining_gift,
                ) = Utils.get_number_remaining_messages(
                    merchant_id,
                    list_block_mess_id,
                    list_gift_code,
                    data_number_mess_license,
                )

                # số mess dc sử dụng tăng thêm số mess mua thêm, quà tặng
                number_mess += number_remaining_mess
                # lấy thông tin sử dụng mess tháng hiện tại
                data_mess_month_now = LicenseMessUsedModel().find_one_license_mess_used(
                    merchant_id, month_get_mess
                )
                # lấy thông tin sử dụng mess tháng trước
                data_mess_last_month = (
                    LicenseMessUsedModel().find_one_license_mess_used(
                        merchant_id, last_month
                    )
                )
                # kiểm tra bản ghi có bị sửa đổi hay ko
                if not Utils.check_data_mess_used(
                    data_mess_month_now
                ) or not Utils.check_data_mess_used(data_mess_last_month):
                    print(
                        "license_sdk::create_number_mess_need_used(): data invalid checksum"
                    )
                    return 0, "data_invalid_checksum", 0

                mess_base_used = 0
                mess_surplus = 0
                if data_mess_month_now:
                    # số mess sử dụng quá trong tháng hiện tại
                    if (
                        data_mess_month_now.get(LicenseMessUsedModel.mess_surplus, 0)
                        > 0
                    ):
                        mess_surplus = data_mess_month_now.get(
                            LicenseMessUsedModel.mess_surplus, 0
                        )
                    # số mess base đã sử dụng trong tháng hiện tại
                    if (
                        data_mess_month_now.get(LicenseMessUsedModel.mess_base_used, 0)
                        > 0
                    ):
                        mess_base_used = data_mess_month_now.get(
                            LicenseMessUsedModel.mess_base_used, 0
                        )
                elif data_mess_last_month:
                    # số mess sử dụng quá trong tháng trước
                    if (
                        data_mess_last_month.get(LicenseMessUsedModel.mess_surplus, 0)
                        > 0
                    ):
                        mess_surplus = data_mess_last_month.get(
                            LicenseMessUsedModel.mess_surplus, 0
                        )
                if mess_surplus > 0:
                    # trừ số lượng dùng quá
                    number_mess = number_mess - mess_surplus
                if mess_base_used > 0:
                    # trừ số lượng base đã sử dụng
                    number_mess = number_mess - mess_base_used
                number_base_percent = round(
                    base_messages_package * Utils.PERCENT_BASE / 100
                )
                if number_mess <= 0:
                    if number_base_percent > 0:
                        if number_mess_need_used and number_mess_need_used > 0:
                            if (
                                number_base_percent
                                >= abs(number_mess) + number_mess_need_used
                            ):
                                number_mess = abs(number_mess)
                                allow_use_mess = 1
                                messages = "base_percent_greater"
                            else:
                                number_mess = 0
                                messages = "number_remaining_mess_not_enough"
                        else:
                            number_mess = 0
                            messages = "mess_not_enough"
                    else:
                        number_mess = 0
                        messages = "not_base_percent_abs_mess"
                elif number_mess_need_used and number_mess_need_used > 0:
                    if number_mess >= number_mess_need_used:
                        allow_use_mess = 1
                        messages = "mess_need_less_mess_allow"
                    else:
                        if number_base_percent > 0:
                            if (
                                number_mess_need_used - number_mess
                            ) <= number_base_percent:
                                allow_use_mess = 1
                                messages = "mess_need_less_base_percent"
                            else:
                                messages = "mess_need_greater_base_percent"
                        else:
                            messages = "not_base_percent"
                if (
                    allow_use_mess
                    and number_mess_need_used
                    and number_mess_need_used > 0
                ):
                    Utils.calculate_mess_sharing_and_save_history(
                        number_mess_need_used,
                        data_mess_month_now,
                        data_mess_last_month,
                        data_remaining_messages,
                        base_messages_package,
                        month_get_mess,
                        list_id_remaining_block,
                        list_id_remaining_gift,
                        merchant_id,
                        child_merchant_id
                    )
            else:
                messages = "license_none"
                print("license_sdk::create_number_mess_need_used(): license none")

        except Exception as ex:
            messages = "error: {}".format(ex)
            print("license_sdk::create_number_mess_need_used():message: {}".format(ex))
        print("license_sdk::create_number_mess_need_used return: number_mess: {}, messages: {}, allow_use_mess: {}".format(number_mess, messages, allow_use_mess))
        return number_mess, messages, allow_use_mess

    @staticmethod
    def calculate_mess_sharing_and_save_history(
        number_mess_need_used,
        data_mess_month_now,
        data_mess_last_month,
        data_remaining_messages,
        base_messages_package,
        month_get_mess,
        list_id_remaining_block,
        list_id_remaining_gift,
        merchant_id,
        child_merchant_id
    ):
        try:
            total_mess_buy = data_remaining_messages.get("total_mess_buy", 0)
            total_mess_gift = data_remaining_messages.get("total_mess_gift", 0)
            if data_mess_month_now:
                mess_base = base_messages_package
                data_mess_month_now[
                    LicenseMessUsedModel.mess_base
                ] = base_messages_package
                mess_base_used = data_mess_month_now.get(
                    LicenseMessUsedModel.mess_base_used, 0
                )
                data_mess_month_now[LicenseMessUsedModel.mess_increase] = total_mess_buy
                mess_increase_used = data_mess_month_now.get(
                    LicenseMessUsedModel.mess_increase_used, 0
                )
                data_mess_month_now[LicenseMessUsedModel.gift] = total_mess_gift
                gift_used = data_mess_month_now.get(LicenseMessUsedModel.gift_used, 0)
                if (mess_base - mess_base_used) >= number_mess_need_used:
                    data_mess_month_now[LicenseMessUsedModel.mess_base_used] = (
                        mess_base_used + number_mess_need_used
                    )
                    Utils.save_history_license_used_mess(data_mess_month_now, child_merchant_id)
                else:
                    data_mess_month_now[LicenseMessUsedModel.mess_base_used] = mess_base
                    number_mess_need_used = number_mess_need_used - (
                        mess_base - mess_base_used
                    )
                    data_detail_mess = []
                    if list_id_remaining_block:
                        for block_id, block_value in list_id_remaining_block.items():
                            if (
                                data_remaining_messages.get(block_id, 0)
                                >= number_mess_need_used
                            ):
                                mess_increase_used = (
                                    mess_increase_used + number_mess_need_used
                                )
                                data_detail_mess.append(
                                    {
                                        LicenseDetailMessUsedModel.mess_type: LicenseDetailMessUsedModel.mess_type_buy,
                                        LicenseDetailMessUsedModel.mess_id: block_id,
                                        LicenseDetailMessUsedModel.number_used: number_mess_need_used,
                                        LicenseDetailMessUsedModel.number_allow_used: block_value,
                                    }
                                )
                                number_mess_need_used = 0
                                break
                            else:
                                mess_increase_used = (
                                    mess_increase_used
                                    + data_remaining_messages.get(block_id, 0)
                                )
                                data_detail_mess.append(
                                    {
                                        LicenseDetailMessUsedModel.mess_type: LicenseDetailMessUsedModel.mess_type_buy,
                                        LicenseDetailMessUsedModel.mess_id: block_id,
                                        LicenseDetailMessUsedModel.number_used: data_remaining_messages.get(
                                            block_id, 0
                                        ),
                                        LicenseDetailMessUsedModel.number_allow_used: block_value,
                                    }
                                )
                                number_mess_need_used = (
                                    number_mess_need_used
                                    - data_remaining_messages.get(block_id, 0)
                                )
                        data_mess_month_now[
                            LicenseMessUsedModel.mess_increase_used
                        ] = mess_increase_used
                    if number_mess_need_used > 0:
                        if list_id_remaining_gift:
                            for block_id, block_value in list_id_remaining_gift.items():
                                if (
                                    data_remaining_messages.get(block_id, 0)
                                    >= number_mess_need_used
                                ):
                                    gift_used = gift_used + number_mess_need_used
                                    data_detail_mess.append(
                                        {
                                            LicenseDetailMessUsedModel.mess_type: LicenseDetailMessUsedModel.mess_type_gift,
                                            LicenseDetailMessUsedModel.mess_id: block_id,
                                            LicenseDetailMessUsedModel.number_used: number_mess_need_used,
                                            LicenseDetailMessUsedModel.number_allow_used: block_value,
                                        }
                                    )
                                    number_mess_need_used = 0
                                    break
                                else:
                                    gift_used = gift_used + data_remaining_messages.get(
                                        block_id, 0
                                    )
                                    data_detail_mess.append(
                                        {
                                            LicenseDetailMessUsedModel.mess_type: LicenseDetailMessUsedModel.mess_type_gift,
                                            LicenseDetailMessUsedModel.mess_id: block_id,
                                            LicenseDetailMessUsedModel.number_used: data_remaining_messages.get(
                                                block_id, 0
                                            ),
                                            LicenseDetailMessUsedModel.number_allow_used: block_value,
                                        }
                                    )
                                    number_mess_need_used = (
                                        number_mess_need_used
                                        - data_remaining_messages.get(block_id, 0)
                                    )
                            data_mess_month_now[
                                LicenseMessUsedModel.gift_used
                            ] = gift_used
                    if number_mess_need_used > 0:
                        data_mess_month_now[LicenseMessUsedModel.mess_surplus] = (
                            data_mess_month_now.get(
                                LicenseMessUsedModel.mess_surplus, 0
                            )
                            + number_mess_need_used
                        )
                    history_id = Utils.save_history_license_used_mess(
                        data_mess_month_now, child_merchant_id
                    )
                    create_on = convert_date_to_format(get_utc_now())
                    for detail_mess in data_detail_mess:
                        detail_mess[LicenseDetailMessUsedModel.history_id] = history_id
                        detail_mess[
                            LicenseDetailMessUsedModel.merchant_id
                        ] = merchant_id
                        detail_mess[LicenseDetailMessUsedModel.month] = month_get_mess
                        detail_mess[LicenseDetailMessUsedModel.create_on] = create_on
                        detail_mess[LicenseDetailMessUsedModel.child_merchant_id] = child_merchant_id
                    LicenseDetailMessUsedModel().insert_many_license_detail_mess_used(
                        data_detail_mess
                    )
            else:
                mess_surplus = 0
                if data_mess_last_month:
                    mess_surplus = data_mess_last_month.get(
                        LicenseMessUsedModel.mess_surplus, 0
                    )
                mess_increase_used = 0
                mess_increase = total_mess_buy
                gift = total_mess_gift
                gift_used = 0
                mess_base = base_messages_package
                mess_base_used = mess_surplus
                mess_surplus = 0
                if (mess_base - mess_base_used) >= number_mess_need_used:
                    mess_base_used += number_mess_need_used
                else:
                    number_mess_need_used = number_mess_need_used - (
                        mess_base - mess_base_used
                    )
                    mess_base_used = mess_base
                    data_detail_mess = []
                    if list_id_remaining_block:
                        for block_id, block_value in list_id_remaining_block.items():
                            if (
                                data_remaining_messages.get(block_id, 0)
                                >= number_mess_need_used
                            ):
                                mess_increase_used = (
                                    mess_increase_used + number_mess_need_used
                                )
                                data_detail_mess.append(
                                    {
                                        LicenseDetailMessUsedModel.mess_type: LicenseDetailMessUsedModel.mess_type_buy,
                                        LicenseDetailMessUsedModel.mess_id: block_id,
                                        LicenseDetailMessUsedModel.number_used: number_mess_need_used,
                                        LicenseDetailMessUsedModel.number_allow_used: block_value,
                                    }
                                )
                                number_mess_need_used = 0
                                break
                            else:
                                mess_increase_used = (
                                    mess_increase_used
                                    + data_remaining_messages.get(block_id, 0)
                                )
                                data_detail_mess.append(
                                    {
                                        LicenseDetailMessUsedModel.mess_type: LicenseDetailMessUsedModel.mess_type_buy,
                                        LicenseDetailMessUsedModel.mess_id: block_id,
                                        LicenseDetailMessUsedModel.number_used: data_remaining_messages.get(
                                            block_id, 0
                                        ),
                                        LicenseDetailMessUsedModel.number_allow_used: block_value,
                                    }
                                )
                                number_mess_need_used = (
                                    number_mess_need_used
                                    - data_remaining_messages.get(block_id, 0)
                                )

                    if number_mess_need_used > 0:
                        if list_id_remaining_gift:
                            for block_id, block_value in list_id_remaining_gift.items():
                                if (
                                    data_remaining_messages.get(block_id, 0)
                                    >= number_mess_need_used
                                ):
                                    gift_used = gift_used + number_mess_need_used
                                    data_detail_mess.append(
                                        {
                                            LicenseDetailMessUsedModel.mess_type: LicenseDetailMessUsedModel.mess_type_gift,
                                            LicenseDetailMessUsedModel.mess_id: block_id,
                                            LicenseDetailMessUsedModel.number_used: number_mess_need_used,
                                            LicenseDetailMessUsedModel.number_allow_used: block_value,
                                        }
                                    )
                                    number_mess_need_used = 0
                                    break
                                else:
                                    gift_used = gift_used + data_remaining_messages.get(
                                        block_id, 0
                                    )
                                    data_detail_mess.append(
                                        {
                                            LicenseDetailMessUsedModel.mess_type: LicenseDetailMessUsedModel.mess_type_gift,
                                            LicenseDetailMessUsedModel.mess_id: block_id,
                                            LicenseDetailMessUsedModel.number_used: data_remaining_messages.get(
                                                block_id, 0
                                            ),
                                            LicenseDetailMessUsedModel.number_allow_used: block_value,
                                        }
                                    )
                                    number_mess_need_used = (
                                        number_mess_need_used
                                        - data_remaining_messages.get(block_id, 0)
                                    )

                    if number_mess_need_used > 0:
                        mess_surplus = number_mess_need_used
                    data_mess_save = {
                        LicenseMessUsedModel.merchant_id: merchant_id,
                        LicenseMessUsedModel.month: month_get_mess,
                        LicenseMessUsedModel.mess_base: mess_base,
                        LicenseMessUsedModel.mess_base_used: mess_base_used,
                        LicenseMessUsedModel.mess_increase: mess_increase,
                        LicenseMessUsedModel.mess_increase_used: mess_increase_used,
                        LicenseMessUsedModel.gift: gift,
                        LicenseMessUsedModel.gift_used: gift_used,
                        LicenseMessUsedModel.mess_surplus: mess_surplus,
                    }
                    history_id = Utils.save_history_license_used_mess(data_mess_save, child_merchant_id)
                    create_on = convert_date_to_format(get_utc_now())
                    for detail_mess in data_detail_mess:
                        detail_mess[LicenseDetailMessUsedModel.history_id] = history_id
                        detail_mess[
                            LicenseDetailMessUsedModel.merchant_id
                        ] = merchant_id
                        detail_mess[LicenseDetailMessUsedModel.month] = month_get_mess
                        detail_mess[LicenseDetailMessUsedModel.create_on] = create_on
                        detail_mess[LicenseDetailMessUsedModel.child_merchant_id] = child_merchant_id
                    LicenseDetailMessUsedModel().insert_many_license_detail_mess_used(
                        data_detail_mess
                    )
        except Exception as ex:
            print(
                "license_sdk::calculate_mess_sharing_and_save_history():message: {}".format(
                    ex
                )
            )

    @staticmethod
    def save_history_license_used_mess(data_mess, child_merchant_id):
        try:
            date_format = convert_date_to_format(get_utc_now())
            check_sum = CryptUtil.encrypt_mobio_crypt2(
                LicenseMessUsedModel().data_mess_to_string(data_mess)
            )
            data_mess[LicenseMessUsedModel.check_sum] = check_sum
            data_history = deepcopy(data_mess)
            data_mess[LicenseMessUsedModel.update_on] = date_format
            LicenseMessUsedModel().upsert_data_mess_used(
                data_mess.get(LicenseMessUsedModel.merchant_id),
                data_mess.get(LicenseMessUsedModel.month),
                data_mess,
            )
            data_history[LicenseHistoryMessUsedModel.history_id] = generate_uuid()
            data_history[
                LicenseHistoryMessUsedModel.create_on
            ] = date_format
            data_history[LicenseHistoryMessUsedModel.child_merchant_id] = child_merchant_id
            LicenseHistoryMessUsedModel().insert_license_history_mess_used(data_history)
            print(
                "license_sdk::save_history_license_used_mess data_history: {}".format(
                    data_history
                )
            )
            return data_history.get(LicenseHistoryMessUsedModel.history_id)
        except Exception as ex:
            print(
                "license_sdk::save_history_license_used_mess():message: {}".format(ex)
            )
            return None

    @staticmethod
    def check_merchant_expire(license_key, merchant_id):
        merchant_expire = True
        try:
            result = CryptUtil.get_license_info(license_key, merchant_id)
            if (
                result
                and result.get("expire_time")
                and convert_timestamp_to_date_utc(result.get("expire_time"))
            ):
                time_stamp_now = convert_date_to_timestamp(get_utc_now())
                if result.get("expire_time") > time_stamp_now:
                    merchant_expire = False
                else:
                    print(
                        "license_sdk::check_time_merchant_expire license merchant expire_time"
                    )
            else:
                print(
                    "license_sdk::check_time_merchant_expire license expire_time not found"
                )
        except Exception as e:
            print("license_sdk::check_time_merchant_expire: ERROR: %s" % e)
        return merchant_expire
