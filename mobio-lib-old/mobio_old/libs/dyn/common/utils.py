import base64
import datetime


class Zone(datetime.tzinfo):
    def __init__(self, offset, isdst, name):
        self.offset = offset
        self.isdst = isdst
        self.name = name

    def utcoffset(self, dt):
        return datetime.timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
        return datetime.timedelta(hours=1) if self.isdst else datetime.timedelta(0)

    def tzname(self, dt):
        return self.name


GMT_7 = Zone(7, False, 'GMT+7')

class Base64(object):
    @staticmethod
    def encode(data):
        try:
            byte_string = data.encode('utf-8')
            encoded_data = base64.b64encode(byte_string)
            return encoded_data.decode(encoding='UTF-8')
        except Exception as ex:
            print('Base64::encode():error: %s' % ex)
            return ""

    @staticmethod
    def decode(encoded_data):
        try:
            if isinstance(encoded_data, bytes):
                encoded_data = encoded_data.decode('UTF-8')
            decoded_data = base64.urlsafe_b64decode(encoded_data + '=' * (-len(encoded_data) % 4))
            return decoded_data.decode(encoding='UTF-8')
        except Exception as ex:
            print('Base64::decode():error: %s' % ex)
            return ''
