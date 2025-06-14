import json
import zlib


def compress_json_content(json_obj: dict[str, list[dict[str, str | float]]]):
    MAGIC_NUMBER = b"blul"
    json_str = json.dumps(json_obj)
    compressed_contents = bytearray()
    compressed_contents.extend(MAGIC_NUMBER)
    compressed_contents.extend(len(json_str).to_bytes(4, byteorder="big", signed=False))
    compressor = zlib.compressobj()
    compressed = compressor.compress(json_str.encode())
    if compressed:
        compressed_contents.extend(compressed)
    compressed_contents.extend(compressor.flush())
    return bytes(compressed_contents)
