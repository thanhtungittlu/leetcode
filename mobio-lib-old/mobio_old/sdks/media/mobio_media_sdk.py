import calendar
import json
import logging
import os
import re
import shutil
import time
import uuid
from datetime import datetime

import magic
from confluent_kafka import Producer
from mobio.libs.Singleton import Singleton
from mobio.libs.caching import LruCache
from mobio.sdks.admin import MobioAdminSDK

from .config import ConsumerTopic, MobioEnvironment, StoreCacheType, Cache
from .constant import DirSaveFile, FieldConstantResponse, CONSTANT_MAP_FORMAT_FILE, ParamMessageSaveInfoFile, \
    ParamMessageUploadMediaSdk, Display
from .custom_mimetypes import CustomMimetypes
from .dir import APP_TMP_DATA_DIR, STATIC_DATA_DIR
from urllib.parse import quote
from mobio.libs.filetypes.file import File as FileExtensionValid
from mobio.libs.filetypes.common import ExtensionImage, ExtensionDocument, ExtensionAudio

logger = logging.getLogger()


@Singleton
class MobioMediaSDK(object):
    lru_cache = None
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 15
    LIST_VERSION_VALID = ["api/v1.0"]
    pattern_domain = r"^(?:http:\/\/|www\.|https:\/\/)([^\/]+)/static/"

    def __init__(self):
        self.folder_static = 'static'
        self.media_api_version = MobioMediaSDK.LIST_VERSION_VALID[-1]

        self.redis_uri = None
        self.admin_host = None
        self.instance = None

    def config(
            self,
            admin_host=None,
            redis_uri=None,
            cache_prefix=None,
            api_media_version=None
    ):
        """
        :param admin_host:
        :param admin_host:
        :param redis_uri: config redis_uri
        :param cache_prefix:
        :param api_media_version:

        :return:
        """
        self.admin_host = admin_host
        if api_media_version:
            self.media_api_version = api_media_version
        if redis_uri:
            self.redis_uri = redis_uri
            if cache_prefix:
                cache_prefix += Cache.PREFIX_KEY
            MobioMediaSDK.lru_cache = LruCache(
                store_type=StoreCacheType.REDIS,
                cache_prefix=cache_prefix,
                redis_uri=redis_uri,
            )
        MobioAdminSDK().config(
            admin_host=self.admin_host,  # admin host
            redis_uri=redis_uri,  # redis uri
            module_use="MEDIA",  # liên hệ admin để khai báo tên của module
            module_encrypt="OaFGfjB6zSvrZQx89Vzn6e120dca106438b69bc5521f757df80f",  # liên hệ admin để lấy mã
        )
        conf = {
            "request.timeout.ms": 20000,
            "bootstrap.servers": MobioEnvironment.KAFKA_BROKER,
        }
        self.instance = Producer(conf)

    @staticmethod
    def valid_input_upload(file_path, file_data, file_byte, merchant_id, expire=None):
        if not merchant_id:
            raise Exception("[ERROR] merchant_id require")
        if not file_path and not file_data and not file_byte:
            raise Exception("[ERROR] Need to pass 1 of 3 parameters file_path or file_data or file_byte")
        if file_path and not os.path.isfile(file_path):
            raise Exception("[ERROR] file_path: {} not exist.".format(file_path))
        if expire:
            try:
                expire = datetime.strptime(expire, "%Y-%m-%dT%H:%M:%SZ")
            except Exception as ex:
                raise Exception("[ERROR] format expire: {} error: {}".format(expire, ex))

    @staticmethod
    def get_file_name(file_path, file_data):
        filename = None
        if file_path:
            head, filename = os.path.split(file_path)
        if file_data:
            try:
                filename = file_data.filename
            except Exception as ex:
                logger.error("[ERROR] file_data: {}".format(ex))
        if not filename:
            filename = str(uuid.uuid4())
        return filename

    @staticmethod
    def validate_file_extension(file_path, extensions_valid=None):
        """
            Kiểm tra xem file có thoải mãn những định dạng cho phép không?
            - Nếu không raise về lỗi
            - Nếu thoả mãn thì cho pass
        """
        if not extensions_valid:
            extensions_valid = ExtensionDocument.LIST_EXTENSION_SUPPORTED + ExtensionImage.LIST_EXTENSION_SUPPORTED + ExtensionAudio.LIST_EXTENSION_SUPPORTED

        result = FileExtensionValid.check_filetype_by_file_extensions(filepath=file_path, extensions=extensions_valid)
        logger.debug("MobioMediaSDK::validate_file_extension:: %s, result :: %s" % (file_path, result))
        if not result or not result.get("status"):
            logger.debug("Remove filepath :: %s" % file_path)
            os.remove(file_path)
            raise Exception("Format file not upload!")



    def upload_without_kafka(
            self,
            merchant_id: str,
            file_path: str = '',
            file_data=None,
            file_byte=None,
            filename: str = '',
            type_media=DirSaveFile.UPLOAD,
            tag: str = '',
            expire=None,
            do_not_delete: bool = False,
            short_link: bool = False,
            desired_format=None,
            display=Display.DISPLAY_SDK,
            group_ids=None,
            extension_isvalid=None
    ):
        """
        :param merchant_id:
        :param file_path:
        :param file_data:
        :param file_byte:
        :param filename:
        :param type_media:
        :param tag:
        :param expire:
        :param do_not_delete
        :param short_link: rút gọn lịnk
        :param desired_format: định dạng mong muốn khi upload
        :param display: Khu vực hiển thị, trong trường hợp không cần hiện thị thì mặc định là no_display_1638219620
        :param group_ids: Danh sách folder cần upload
        :param extension_isvalid: Danh sách extension muốn kiểm tra.

        "return:
        {
            "url": "",
            "local_host":""
        }
        """
        MobioMediaSDK.valid_input_upload(
            file_path=file_path,
            file_data=file_data,
            file_byte=file_byte,
            merchant_id=merchant_id,
            expire=expire
        )

        time_start = time.time()
        mimetype_str = MobioMediaSDK.get_mimetype(file_path=file_path, file_data=file_data, file_byte=file_byte)
        MobioMediaSDK.validate_desired_format(desired_format=desired_format, mimetype_str=mimetype_str)

        if not filename:
            filename = MobioMediaSDK.get_file_name(file_path=file_path, file_data=file_data)
        host_by_merchant_id = self._get_host_by_merchant_id(merchant_id=merchant_id)
        logger.debug("upload_without_kafka()::get_host_by_merchant_id:: %s" % (time.time() - time_start))
        dist_file, filename = self.create_dir_save_file(
            folder=STATIC_DATA_DIR,
            merchant_id=merchant_id,
            type_media=type_media,
            filename=filename,
            short_link=short_link
        )
        if file_path:
            # shutil.move(file, dist_file)
            shutil.move(file_path, dist_file)
        elif file_data:
            file_data.save(dist_file)
        else:
            with open(dist_file, "wb") as f:
                f.write(file_byte)

        MobioMediaSDK.validate_file_extension(dist_file, extension_isvalid)
        from .utils import file_capacity, convert_bytes
        capacity = convert_bytes(file_capacity(dist_file))
        decode_filename = quote(filename)
        url = os.path.join(host_by_merchant_id, self.folder_static, merchant_id, type_media, decode_filename)
        if short_link:
            url = os.path.join(host_by_merchant_id, self.folder_static, decode_filename)
        logger.debug("upload_without_kafka()::url:: %s" % (time.time() - time_start))
        data_send_producer = {
            ParamMessageSaveInfoFile.FILENAME: filename,
            ParamMessageSaveInfoFile.MERCHANT_ID: merchant_id,
            ParamMessageSaveInfoFile.URL: url,
            ParamMessageSaveInfoFile.TYPE_MEDIA: type_media,
            ParamMessageSaveInfoFile.TAG: tag,
            ParamMessageSaveInfoFile.EXPIRE: expire,
            ParamMessageSaveInfoFile.DIST_FILE: dist_file,
            ParamMessageSaveInfoFile.MIMETYPE_STR: mimetype_str,
            ParamMessageSaveInfoFile.DO_NOT_DELETE: do_not_delete,
            ParamMessageSaveInfoFile.GROUP_IDS: group_ids,
            ParamMessageSaveInfoFile.DISPLAY: display
        }

        self.send_message_to_topic(topic=ConsumerTopic.TOPIC_SAVE_INFO_MEDIA_SDK, data=json.dumps(data_send_producer))
        logger.debug("upload_without_kafka()::send message to topic:: %s" % (time.time() - time_start))
        return {
            FieldConstantResponse.URL: url,
            FieldConstantResponse.LOCAL_PATH: dist_file,
            FieldConstantResponse.FILENAME: filename,
            FieldConstantResponse.FORMAT: mimetype_str,
            FieldConstantResponse.CAPACITY: capacity
        }

    def upload_with_kafka(
            self,
            merchant_id,
            file_path: str = None,
            file_data=None,
            file_byte=None,
            filename=None,
            type_media=DirSaveFile.UPLOAD,
            tag=None,
            expire=None,
            do_not_delete=False,
            short_link=False,
            desired_format=None,
            display=Display.DISPLAY_SDK,
            group_ids=None,
            extension_isvalid=None
    ):
        """
        :param merchant_id:
        :param filename:
        :param file_path:
        :param file_byte:
        :param file_data:
        :param filename:
        :param type_media:
        :param tag:
        :param expire:
        :param do_not_delete:
        :param short_link:
        :param desired_format: định dạng mong muốn khi upload
        :param display: Khu vực hiển thị, trong trường hợp không cần hiện thị thì mặc định là no_display_1638219620
        :param group_ids: Danh sách folder cần upload
        :param extension_isvalid: Danh sách extension muốn kiểm tra.

        :return:
        {
        }
        """
        MobioMediaSDK.valid_input_upload(
            file_path=file_path,
            file_data=file_data,
            file_byte=file_byte,
            merchant_id=merchant_id,
            expire=expire
        )

        time_start = time.time()
        mimetype_str = MobioMediaSDK.get_mimetype(file_path=file_path, file_data=file_data, file_byte=file_byte)
        MobioMediaSDK.validate_desired_format(desired_format=desired_format, mimetype_str=mimetype_str)
        if not filename:
            filename = MobioMediaSDK.get_file_name(file_path=file_path, file_data=file_data)

        tmp_file, filename = self.create_dir_save_file(
            folder=APP_TMP_DATA_DIR,
            merchant_id=merchant_id,
            type_media=type_media,
            filename=filename
        )

        if file_path:
            # shutil.move(file, tmp_file)
            shutil.move(file_path, tmp_file)
        elif file_data:
            file_data.save(tmp_file)
        else:
            with open(tmp_file, "wb") as f:
                f.write(file_byte)
        MobioMediaSDK.validate_file_extension(tmp_file, extension_isvalid)
        from .utils import file_capacity, convert_bytes
        capacity = convert_bytes(file_capacity(tmp_file))
        logger.debug("upload_with_kafka()::move file:: %s" % (time.time() - time_start))
        dist_file, filename = self.create_dir_save_file(
            folder=STATIC_DATA_DIR,
            merchant_id=merchant_id,
            type_media=type_media,
            filename=filename,
            short_link=short_link
        )
        host_by_merchant_id = self._get_host_by_merchant_id(merchant_id=merchant_id)
        logger.debug("upload_with_kafka()::get_host_by_merchant_id:: %s" % (time.time() - time_start))
        decode_filename = quote(filename)
        url = os.path.join(host_by_merchant_id, self.folder_static, merchant_id, type_media, decode_filename)
        if short_link:
            url = os.path.join(host_by_merchant_id, self.folder_static, decode_filename)
        data_send_producer = {
            ParamMessageUploadMediaSdk.FILENAME: filename,
            ParamMessageUploadMediaSdk.MERCHANT_ID: merchant_id,
            ParamMessageUploadMediaSdk.TMP_FILE: tmp_file,
            ParamMessageUploadMediaSdk.TYPE_MEDIA: type_media,
            ParamMessageUploadMediaSdk.TAG: tag,
            ParamMessageUploadMediaSdk.EXPIRE: expire,
            ParamMessageUploadMediaSdk.DIST_FILE: dist_file,
            ParamMessageUploadMediaSdk.MIMETYPE_STR: mimetype_str,
            ParamMessageUploadMediaSdk.DO_NOT_DELETE: do_not_delete,
            ParamMessageUploadMediaSdk.URL: url,
            ParamMessageUploadMediaSdk.GROUP_IDS: group_ids,
            ParamMessageUploadMediaSdk.DISPLAY: display
        }
        self.send_message_to_topic(topic=ConsumerTopic.TOPIC_UPLOAD_MEDIA_SDK, data=json.dumps(data_send_producer))
        logger.debug("upload_with_kafka()::send message to topic:: %s" % (time.time() - time_start))
        return {
            FieldConstantResponse.URL: url,
            FieldConstantResponse.LOCAL_PATH: dist_file,
            FieldConstantResponse.FILENAME: filename,
            FieldConstantResponse.FORMAT: mimetype_str,
            FieldConstantResponse.CAPACITY: capacity,
        }

    def create_public_url_without_file(
            self,
            merchant_id,
            filename=None,
            type_media=DirSaveFile.UPLOAD,
            tag=None,
            expire=None,
            do_not_delete=False,
            short_link=False,
            mimetype_str=None,
            display=Display.DISPLAY_SDK,
            group_ids=None

    ):
        dist_file, filename = self.create_dir_save_file(
            folder=STATIC_DATA_DIR,
            merchant_id=merchant_id,
            type_media=type_media,
            filename=filename,
            short_link=short_link
        )
        host_by_merchant_id = self._get_host_by_merchant_id(merchant_id=merchant_id)
        logger.info("create_public_url_without_file :: host_by_merchant_id :: %s " % host_by_merchant_id)
        decode_filename = quote(filename)
        url = os.path.join(host_by_merchant_id, self.folder_static, merchant_id, type_media, decode_filename)
        if short_link:
            url = os.path.join(host_by_merchant_id, self.folder_static, decode_filename)
        logger.info("create_public_url_without_file :: url :: %s " % url)
        logger.info("create_public_url_without_file :: local_path :: %s " % dist_file)
        time_start = time.time()
        data_send_producer = {
            ParamMessageSaveInfoFile.FILENAME: filename,
            ParamMessageSaveInfoFile.MERCHANT_ID: merchant_id,
            ParamMessageSaveInfoFile.URL: url,
            ParamMessageSaveInfoFile.TYPE_MEDIA: type_media,
            ParamMessageSaveInfoFile.TAG: tag,
            ParamMessageSaveInfoFile.EXPIRE: expire,
            ParamMessageSaveInfoFile.DIST_FILE: dist_file,
            ParamMessageSaveInfoFile.DO_NOT_DELETE: do_not_delete,
            ParamMessageSaveInfoFile.MIMETYPE_STR: mimetype_str,
            ParamMessageSaveInfoFile.NOT_CHECK_PATH_EXISTS: True,
            ParamMessageSaveInfoFile.GROUP_IDS: group_ids,
            ParamMessageSaveInfoFile.DISPLAY: display
        }

        self.send_message_to_topic(topic=ConsumerTopic.TOPIC_SAVE_INFO_MEDIA_SDK, data=json.dumps(data_send_producer))
        logger.debug("upload_without_kafka()::send message to topic:: %s" % (time.time() - time_start))
        return {
            FieldConstantResponse.URL: url,
            FieldConstantResponse.LOCAL_PATH: dist_file,
            FieldConstantResponse.FILENAME: filename
        }

    def finish_save_file_by_public_url(self, filepath=None, file_data=None, file_byte=None, url=None):
        if not url:
            raise Exception("[ERROR] :: url not None")
        local_path = self.get_path_by_url(url, is_check_path_exists=False)
        logger.info("finish_save_file_by_url :: get_path_by_url % s result :: %s " % (url, local_path))
        if filepath:
            shutil.move(filepath, local_path)
        elif file_data:
            file_data.save(local_path)
        else:
            with open(local_path, "wb") as f:
                f.write(file_byte)

    @classmethod
    def create_dir_save_file(cls, folder, merchant_id, type_media, filename, short_link=False):
        dir_file = os.path.join(folder, merchant_id)
        if type_media:
            dir_file = os.path.join(folder, merchant_id, type_media)
        if short_link:
            dir_file = folder
        os.makedirs(dir_file, exist_ok=True)
        local_path = os.path.join(dir_file, filename)
        if os.path.isfile(local_path):
            filename = str(calendar.timegm(time.gmtime())) + "_" + filename
            local_path = os.path.join(dir_file, filename)
        return local_path, filename

    @staticmethod
    def validate_desired_format(desired_format, mimetype_str):
        if not desired_format or desired_format == "all":
            return True
        all_format_desired = CONSTANT_MAP_FORMAT_FILE.get(desired_format)
        if (not all_format_desired) or (mimetype_str not in all_format_desired):
            extension = CustomMimetypes().mimetypes.guess_extension(mimetype_str)
            raise Exception(
                "[ERROR] File định dạng {}, không đúng định dạng mong muốn là {}".format(extension, desired_format))

    def get_path_by_url(
            self,
            url,
            is_check_path_exists=True
    ):
        if not url:
            raise ValueError("[ERROR] URL not none")
        try:
            local_path = re.sub(self.pattern_domain, STATIC_DATA_DIR + "/", url)
        except Exception as ex:
            logger.error("[ERROR] get local_path_file error %s " % ex)
            raise Exception("url %s not found" % url)
        if is_check_path_exists and not os.path.isfile(local_path):
            raise Exception("[ERROR] local_path :: %s not exists" % local_path)
        return local_path

    def get_binary_by_url(self, url):
        local_path = self.get_path_by_url(url)
        with open(local_path, "rb") as f:
            return f.read()

    def get_filename_by_url(self, url):
        local_path = self.get_path_by_url(url)
        filename = os.path.basename(local_path)
        return filename

    def create_filepath(
            self,
            merchant_id: str,
            filename: str = None,
            type_media: str = DirSaveFile.DOWNLOAD
    ):
        return self.create_dir_save_file(
            folder=STATIC_DATA_DIR,
            merchant_id=merchant_id,
            type_media=type_media,
            filename=filename
        )

    def check_type_media(self, type_media):
        if type_media not in [DirSaveFile.UPLOAD, DirSaveFile.DOWNLOAD]:
            raise ValueError("Type media is not correct!")
        return type_media

    def _get_host_by_merchant_id(self, merchant_id):
        from .utils import get_host_by_merchant_id
        host_by_merchant_id = get_host_by_merchant_id(
            admin_host=self.admin_host,
            merchant_id=merchant_id,
            media_api_version=self.media_api_version,
            request_timeout=self.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )
        if not host_by_merchant_id:
            return MobioEnvironment.PUBLIC_HOST
        return host_by_merchant_id

    @staticmethod
    def get_mimetype(file_data, file_path, file_byte):
        mimetype_str = None
        if file_path and os.path.isfile(file_path):
            magic_init = magic.Magic(mime=True)
            mimetype_str = magic_init.from_file(file_path)
        elif file_data:
            mimetype_str = file_data.mimetype if file_data.mimetype else file_data.content_type
        elif file_byte:
            magic_init = magic.Magic(mime=True)
            mimetype_str = magic_init.from_buffer(file_byte)
        logger.info("mimetype_str:: %s" % mimetype_str)
        return mimetype_str

    def override_file(
            self,
            filename=None,
            merchant_id=None,
            url="",
            file_path=None,
            file_data=None,
            file_byte=None,
            desired_format=None
    ):
        MobioMediaSDK.valid_input_upload(
            file_path=file_path,
            file_data=file_data,
            file_byte=file_byte,
            merchant_id=merchant_id
        )
        mimetype_str = MobioMediaSDK.get_mimetype(file_path=file_path, file_data=file_data, file_byte=file_byte)
        MobioMediaSDK.validate_desired_format(desired_format=desired_format, mimetype_str=mimetype_str)
        time_start = time.time()
        # mimetype_str = self._get_mimetype(file)
        tmp_file, filename = self.create_dir_save_file(
            folder=APP_TMP_DATA_DIR,
            merchant_id=merchant_id,
            type_media=DirSaveFile.UPLOAD,
            filename=filename
        )
        if file_path:
            shutil.move(file_path, tmp_file)
        else:
            file_data.save(tmp_file)
        logger.debug("override_file()::move file:: %s" % (time.time() - time_start))
        data_send_producer = {
            "merchant_id": merchant_id,
            "url_override": url,
            "path_temp_file": tmp_file
        }

        self.send_message_to_topic(
            topic=ConsumerTopic.TOPIC_OVERRIDE_MEDIA_SDK,
            data=json.dumps(data_send_producer)
        )
        logger.debug("override_file()::send message to topic:: %s" % (time.time() - time_start))

    def delete_file(
            self,
            merchant_id,
            urls,
            type_delete=None
    ):
        if not urls:
            logger.error("[ERROR] urls empty")
            return None

        data_send_producer = {
            "merchant_id": merchant_id,
            "urls": urls,
            "type_delete": type_delete
        }
        self.send_message_to_topic(
            topic=ConsumerTopic.TOPIC_DELETE_MEDIA_SDK,
            data=json.dumps(data_send_producer)
        )

    def send_message_to_topic(self, topic: str, data):
        self.instance.produce(topic, data)
        self.instance.poll(0)
        logger.info("topic: {}, message: {}".format(topic, data))
        self.instance.flush()
