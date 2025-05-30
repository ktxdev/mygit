import os
import zlib
import hashlib

from typing import Union

from objects.object import write_object
from utils.constants import REPO_DIR_NAME, OBJECTS_DIR_NAME

def add_blob_header(content: bytes) -> bytes:
    header = f"blob {len(content)}\0".encode()
    return header + content

def get_blob_sha1(content: bytes) -> str:
    content = add_blob_header(content)
    return hashlib.sha1(content).hexdigest()


def write_blob(content: bytes) -> str:
    blob_sha1 = get_blob_sha1(content)
    content = add_blob_header(content)

    write_object(content, blob_sha1)

    return blob_sha1



    
    
    
    