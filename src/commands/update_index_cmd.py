import os
import zlib

from utils.constants import VALID_BLOB_OR_TREE_MODES, REPO_DIR_NAME, INDEX_FILE_NAME
from objects.object import is_blob_object, is_tree_object
from index import update_index_entry
from commands.hash_object_cmd import hash_object_cmd

class BlobError(Exception):
    pass

def update_index_from_file(filename: str):
    # TODO: set mode based on file type
    sha1_hex = hash_object_cmd(filename, True)
    update_index_entry(100644, 0, sha1_hex, filename)
    

def update_index_from_cache(mode: str, sha1_hex: str, filename: str):
    if mode not in VALID_BLOB_OR_TREE_MODES:
        raise BlobError('Invalid mode') 
    

    if not is_blob_object(sha1_hex) and not is_tree_object(sha1_hex):
        raise  BlobError('Provided sha-1 is not for a blob or tree object')

    update_index_entry(mode, 0, sha1_hex, filename)

