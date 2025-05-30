import os
import hashlib

from objects.blob import write_blob, get_blob_sha1

def hash_object_cmd(input: str, write: bool) -> str:
    """
    Hashes an object and writes it to the objects directory.
    """
    is_file = isinstance(input, str) and os.path.isfile(input)
    
    if is_file:
        with open(input, "rb") as f:
            content = f.read()
    else:
        content = input.encode() if isinstance(input, str) else input

    sha1_hex = get_blob_sha1(content)

    if write:
        sha1_hex = write_blob(content)
        
    return sha1_hex