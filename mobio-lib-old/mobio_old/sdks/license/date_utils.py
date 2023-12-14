import uuid
import datetime




def ConvertDateUTCtoStringITC(date_input_time, tz_minute, dinhdang="%H:%M %d/%m/%Y"):
    try:
        thoi_gian_itc = date_input_time + datetime.timedelta(minutes=tz_minute)
        return thoi_gian_itc.strftime(dinhdang)
    except:
        return ""


def convert_date_to_format(vNgayThang, format="%Y%m%d%H%M%S"):
    try:
        if vNgayThang is not None:
            return vNgayThang.strftime(format)
        else:
            return ""
    except:
        return ""


def convert_str_to_date(date_str, format="%Y%m%d%H%M%S"):
    try:
        return datetime.datetime.strptime(date_str, format).replace(
            tzinfo=datetime.timezone.utc
        )
    except:
        return None


def get_utc_now():
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    return now


def convert_timestamp_to_date_utc(timestamp):
    try:
        if timestamp is not None:
            return datetime.datetime.utcfromtimestamp(timestamp).replace(
                tzinfo=datetime.timezone.utc
            )
        else:
            return None
    except:
        return None


def convert_date_utc_to_date_itc(date_input_time, tz_minute):
    try:
        thoi_gian_itc = date_input_time + datetime.timedelta(minutes=tz_minute)
        return thoi_gian_itc
    except:
        return None


def convert_date_to_timestamp(vNgayThang):
    try:
        if vNgayThang is not None:
            return round(vNgayThang.replace(tzinfo=datetime.timezone.utc).timestamp())
        else:
            return None
    except:
        return None


def generate_uuid():
    return str(uuid.uuid1())
