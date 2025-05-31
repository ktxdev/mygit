import os
import zlib

from utils.constants import REPO_DIR_NAME, OBJECTS_DIR_NAME


def read_object(sha1_hex: str) -> bytes:
    object_dir_path = os.path.join(os.getcwd(), REPO_DIR_NAME, OBJECTS_DIR_NAME, sha1_hex[:2])
    object_file_path = os.path.join(object_dir_path, sha1_hex[2:])

    with open(object_file_path, "rb") as f:
        compressed_data = f.read()

    return zlib.decompress(compressed_data)

def write_object(content: bytes, sha1_hex: str) -> str:
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

def get_object_type(sha1_hex: str) -> str:
    content = read_object(sha1_hex)

    header, _ = content.decode().split("\0", 1)
    object_type, _ = header.split(" ")

    return object_type

def get_object_content(sha1_hex: str) -> bytes:
    content = read_object(sha1_hex)

    _, content = content.decode().split("\0", 1)

    return content

def is_blob_object(sha1_hex: str) -> bool:
    return get_object_type(sha1_hex) == "blob"

def is_tree_object(sha1_hex: str) -> bool:
    return get_object_type(sha1_hex) == "tree"