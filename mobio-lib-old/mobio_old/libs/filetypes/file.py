import logging
import os

from mobio.libs.filetypes.common import ExtensionDocument, ExtensionAudio, ExtensionImage
# from ..filetypes.utils import read_file_to_hex_data_by_path, load_signature_by_hex_data, \
#     read_file_to_hex_data_by_file_binary, get_max_offset_extensions
from mobio.libs.filetypes.utils import read_file_to_hex_data_by_path, load_signature_by_hex_data, \
    read_file_to_hex_data_by_file_binary, get_max_offset_extensions

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class File(object):

    def __init__(self):
        pass

    @staticmethod
    def validate_input_filepath(filepath):
        if not os.path.isfile(filepath):
            message = "[ERROR] :: filepath %s not exist." % filepath
            logger.error(message)
            raise Exception(message)
        return

    @staticmethod
    def validate_input_extension(extensions):
        if not extensions:
            logger.error("extensions must be exists")
            raise Exception("[ERROR]")
        return

    @staticmethod
    def get_extension_by_filepath(filepath, max_offset_extensions):
        # Validate filepath
        File.validate_input_filepath(filepath)
        hex_data_file = read_file_to_hex_data_by_path(filepath, max_offset_extensions)
        # logger.debug("get_extension_by_filepath :: hex_data_file :: %s" % str(hex_data_file))
        lst_extension = load_signature_by_hex_data(hex_data_file)
        logger.debug("get_extension_by_filepath :: lst_extension :: %s" % str(lst_extension))
        return lst_extension

    @staticmethod
    def get_extension_by_file_binary(file_binary, max_offset_extensions):
        # Validate filepath
        hex_data_file = read_file_to_hex_data_by_file_binary(file_binary, max_offset_extensions)
        # logger.debug("get_extension_by_file_binary :: hex_data_file :: %s" % str(hex_data_file))
        lst_extension = load_signature_by_hex_data(hex_data_file)
        logger.debug("get_extension_by_file_binary :: lst_extension :: %s" % str(lst_extension))
        return lst_extension

    @staticmethod
    def check_filetype_by_file_extensions(filepath=None, file_binary=None, extensions=None):
        File.validate_input_extension(extensions)
        logger.debug("check_filetype_by_file_extensions :: filepath :: %s" % str(filepath))
        # logger.debug("check_filetype_by_file_extensions :: file_binary :: %s" % str(file_binary))
        logger.debug("check_filetype_by_file_extensions :: extensions :: %s" % str(extensions))

        max_offset_extensions = get_max_offset_extensions(extensions)
        logger.debug("check_filetype_by_file_extensions :: max_offset_extensions :: %s" % str(max_offset_extensions))

        if filepath:
            lst_extension = File.get_extension_by_filepath(filepath, max_offset_extensions)
        else:
            lst_extension = File.get_extension_by_file_binary(file_binary, max_offset_extensions)
        result_merge_extension = list(set(lst_extension) & set(extensions))
        result = {
            "status": len(result_merge_extension) > 0,
            "extension_of_file": lst_extension
        }
        return result


if __name__ == '__main__':
    lst_extension_support = ExtensionAudio.LIST_EXTENSION_SUPPORTED + ExtensionDocument.LIST_EXTENSION_SUPPORTED + ExtensionImage.LIST_EXTENSION_SUPPORTED

    result = File.check_filetype_by_file_extensions(
        "/Users/tungdd/Downloads/sample1.heif",
        extensions=lst_extension_support
    )
    print(result)
