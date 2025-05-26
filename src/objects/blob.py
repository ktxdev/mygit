import os
import zlib

from typing import Union

from src.utils.hash import encode_content
from src.utils.constants import REPO_DIR_NAME, OBJECTS_DIR_NAME


def write_blob(source: Union[str, bytes], chunk_size: int = 8192) -> str:
    # Determine if the source is a file path or content
    is_file = isinstance(source, str) and os.path.isfile(source)

    if is_file:
        with open(source, "rb") as f:
            content = f.read()
    else:
        content = source.encode() if isinstance(source, str) else source
    
    sha1_hex = encode_content(content)

    # Compress the content
    compressed_content = zlib.compress(content)
    
    # Write to .mygit/objects
    object_dir_path = os.path.join(os.getcwd(), REPO_DIR_NAME, OBJECTS_DIR_NAME, sha1_hex[:2])
    object_file_path = os.path.join(object_dir_path, sha1_hex[2:])

    # create the object directory if it doesn't exist
    os.makedirs(object_dir_path, exist_ok=True)

    # write the compressed content to the object file
    with open(object_file_path, "wb") as f:
        f.write(compressed_content)

    return sha1_hex

def read_blob(sha1_hex: str) -> bytes:
    object_dir_path = os.path.join(os.getcwd(), REPO_DIR_NAME, OBJECTS_DIR_NAME, sha1_hex[:2])
    object_file_path = os.path.join(object_dir_path, sha1_hex[2:])

    with open(object_file_path, "rb") as f:
        compressed_data = f.read()

    # Decompress the content
    data = zlib.decompress(compressed_data)

    return data.decode() if isinstance(data, bytes) else data

    
    
    
    