import binascii
import json

from ..filetypes.common import FILEPATH_SIGNATURE, ParamFileSignature


def read_file_to_hex_data_by_path(filepath, max_offset_extensions):
    # Open in binary mode (so you don't read two byte line endings on Windows as one byte)
    # and use with statement (always do this to avoid leaked file descriptors, unflushed files)
    with open(filepath, 'rb') as f:
        # Slurp the whole file and efficiently convert it to hex all at once
        hex_data = binascii.hexlify(f.read(max_offset_extensions))
    return hex_data


def read_file_to_hex_data_by_file_binary(file_binary, max_offset_extensions):
    stream_read = file_binary.stream.read()
    file_binary.seek(0)
    hex_data = binascii.hexlify(stream_read)
    return hex_data


def load_signature_by_hex_data(hex_data_file):
    results = []
    with open(FILEPATH_SIGNATURE, "r") as f:
        data_signature = f.read()
        data_signature = json.loads(data_signature)
        for extension, signature in data_signature.items():
            lst_signs = signature.get(ParamFileSignature.SIGNS)
            for sign_data in lst_signs:
                signs = sign_data.split(",")
                offset, hex_code = int(signs[0]), signs[1]
                len_hex_code = len(hex_code)
                switch_index = int(offset) >= 0
                target_index = int(offset) + len_hex_code if switch_index else int(offset) - len_hex_code

                start_index = int(offset) if switch_index else target_index
                end_index = target_index if switch_index else int(offset)

                hex_data_slice = hex_data_file[start_index: end_index].decode('utf-8')
                if hex_code.lower() == hex_data_slice.lower() and extension not in results:
                    results.append(extension)
    return results


def get_max_offset_extensions(extensions):
    max_offset_extensions = 0
    with open(FILEPATH_SIGNATURE, "r") as f:
        data_signature = f.read()
        data_signature = json.loads(data_signature)
        for extension, signature in data_signature.items():
            if extension not in extensions:
                continue
            lst_signs = signature.get(ParamFileSignature.SIGNS)
            for sign_data in lst_signs:
                signs = sign_data.split(",")
                offset, hex_code = int(signs[0]), signs[1]
                len_hex_code = len(hex_code)

                if len_hex_code > max_offset_extensions:
                    max_offset_extensions = len_hex_code
    return max_offset_extensions
