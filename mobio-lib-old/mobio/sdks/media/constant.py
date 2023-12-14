class DirSaveFile:
    UPLOAD = "upload"
    DOWNLOAD = "download"


class FieldConstantResponse:
    URL = "url"
    LOCAL_PATH = "local_path"
    FILENAME = "filename"
    FORMAT = "format"
    CAPACITY = "capacity"


class ParamMessage:
    FILENAME = "filename"
    MERCHANT_ID = "merchant_id"
    URL = "url"
    TYPE_MEDIA = "type_media"
    TAG = "tag"
    EXPIRE = "expire"
    DIST_FILE = "dist_file"
    DO_NOT_DELETE = "do_not_delete"
    MIMETYPE_STR = "mimetype_str"
    DISPLAY = "display"
    GROUP_IDS = "group_ids"


class ParamMessageSaveInfoFile(ParamMessage):
    NOT_CHECK_PATH_EXISTS = "not_check_path_exists"


class ParamMessageUploadMediaSdk(ParamMessage):
    TMP_FILE = "tmp_file"


class Display:
    DISPLAY_SDK = "display_sdk_1638219620"
    LIST = "LIST"


class ParamPayload:
    X_MERCHANT_ID = "X-Merchant-ID"
    FILE = "file"
    WITH_EXTENSION = "with_extension"
    USE_NAME = "use_name"
    FILE_NAME = "filename"
    GROUP_IDS = "group_ids"
    EXPIRE = "expire"
    TAGS = "tags"
    DO_NOT_DELETE = "do_not_delete"
    FILETYPE = "filetype"
    DISPLAY = "display"
    DESIRED_FORMAT = "desired_format"


CONSTANT_MAP_FORMAT_FILE = {
    "image": [
        'image/bmp', 'image/gif', 'image/ief', 'image/jpeg', 'image/jpeg', 'image/jpeg', 'image/png',
        'image/svg+xml', 'image/tiff', 'image/tiff', 'image/x-icon', 'image/x-cmu-raster',
        'image/x-portable-anymap', 'image/x-portable-bitmap', 'image/x-portable-graymap',
        'image/x-portable-pixmap', 'image/x-rgb', 'image/x-xbitmap', 'image/x-xpixmap', 'image/x-xwindowdump',
        'image/cgm', 'image/g3fax', 'image/jp2', 'image/ktx', 'image/pict', 'image/x-pict', 'image/x-pict',
        'image/prs.btif', 'image/sgi', 'image/svg+xml', 'image/vnd.adobe.photoshop', 'image/vnd.dece.graphic',
        'image/vnd.dece.graphic', 'image/vnd.dece.graphic', 'image/vnd.dece.graphic', 'image/vnd.djvu',
        'image/vnd.djvu', 'image/vnd.dwg', 'image/vnd.dxf', 'image/vnd.fastbidsheet', 'image/vnd.fpx',
        'image/vnd.fst', 'image/vnd.fujixerox.edmics-mmr', 'image/vnd.fujixerox.edmics-rlc', 'image/vnd.ms-modi',
        'image/vnd.ms-photo', 'image/vnd.net-fpx', 'image/vnd.wap.wbmp', 'image/vnd.xiff', 'image/webp',
        'image/x-3ds', 'image/x-cmx', 'image/x-freehand', 'image/x-freehand', 'image/x-freehand',
        'image/x-freehand', 'image/x-freehand', 'image/x-macpaint', 'image/x-macpaint', 'image/x-macpaint',
        'image/x-mrsid-image', 'image/x-pcx', 'image/x-quicktime', 'image/x-quicktime', 'image/x-tga'
    ],
    "video": [
        'video/mp4', 'video/mpeg', 'video/mpeg', 'video/mpeg', 'video/mpeg', 'video/mpeg', 'video/quicktime',
        'video/quicktime', 'video/webm', 'video/x-msvideo', 'video/x-sgi-movie', 'video/3gpp', 'video/3gpp2',
        'video/h261', 'video/h263', 'video/h264', 'video/jpeg', 'video/jpm', 'video/jpm', 'video/mj2',
        'video/mj2', 'video/mp2t', 'video/mp4', 'video/mp4', 'video/x-m4v', 'video/mpeg', 'video/ogg',
        'video/vnd.dece.hd', 'video/vnd.dece.hd', 'video/vnd.dece.mobile', 'video/vnd.dece.mobile',
        'video/vnd.dece.pd', 'video/vnd.dece.pd', 'video/vnd.dece.sd', 'video/vnd.dece.sd',
        'video/vnd.dece.video', 'video/vnd.dece.video', 'video/vnd.dvb.file', 'video/vnd.fvt',
        'video/vnd.mpegurl', 'video/vnd.mpegurl', 'video/vnd.ms-playready.media.pyv', 'video/vnd.uvvu.mp4',
        'video/vnd.uvvu.mp4', 'video/vnd.vivo', 'video/x-dv', 'video/x-dv', 'video/x-f4v', 'video/x-fli',
        'video/x-flv', 'video/x-matroska', 'video/x-matroska', 'video/x-matroska', 'video/x-mng',
        'video/x-ms-asf', 'video/x-ms-asf', 'video/x-ms-vob', 'video/x-ms-wm', 'video/x-ms-wmv', 'video/x-ms-wmx',
        'video/x-ms-wvx', 'video/x-smv'
    ],
    "excel": [
        'application/vnd.ms-excel', 'application/vnd.ms-excel', 'application/vnd.ms-excel', 'application/vnd.ms-excel',
        'application/vnd.ms-excel', 'application/vnd.ms-excel', 'application/vnd.ms-excel',
        'application/vnd.ms-excel.addin.macroenabled.12', 'application/vnd.ms-excel.sheet.binary.macroenabled.12',
        'application/vnd.ms-excel.sheet.macroenabled.12', 'application/vnd.ms-excel.template.macroenabled.12'
    ],
    "html": ['text/html'],
    "text": ['text/plain'],
    "word": ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']
}
