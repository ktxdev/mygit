import os
import zlib

from src.utils.constants import VALID_BLOB_MODES, REPO_DIR_NAME, INDEX_FILE_NAME
from src.objects.blob import is_blob_object
from src.index import update_index_entry

class BlobError(Exception):
    pass

def uodate_index_from_cache(mode: str, sha1_hex: str, filename: str):
    if mode not in VALID_BLOB_MODES:
        raise BlobError('Invalid mode')
    

    if not is_blob_object(sha1_hex):
        raise  BlobError('Provided sha-1 is not for a blob object')

    update_index_entry(mode, 0, sha1_hex, filename)

