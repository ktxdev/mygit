import os
import hashlib

from src.objects.blob import write_blob

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

    sha1_hex = hashlib.sha1(content).hexdigest()

    if write:
        write_blob(content, sha1_hex)
        
    return sha1_hex