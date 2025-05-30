import os
import zlib

from src.utils.constants import VALID_BLOB_MODES, REPO_DIR_NAME, INDEX_FILE_NAME
from src.objects.blob import is_blob_object
from src.index import get_index_entries

class BlobError(Exception):
    pass

def add_or_update_entry(entries: list[bytes], mode: str, stage_number: int, sha1_hex: str, filename: str):
    updated_entries = []
    entry_exists = False

    for entry in entries:
        if entry.split(b' ')[1].decode() == filename:
            updated_entries.append(f"{mode} {filename} {stage_number} {sha1_hex}\n".encode())
            entry_exists = True
        else:
            updated_entries.append(entry)

    if not entry_exists:
        updated_entries.append(f"{mode} {filename} {stage_number} {sha1_hex}\n".encode())
    return updated_entries

def add_index_from_cache(mode: str, sha1_hex: str, filename: str):
    if mode not in VALID_BLOB_MODES:
        raise BlobError('Invalid mode')
    

    if not is_blob_object(sha1_hex):
        raise  BlobError('Provided sha-1 is not for a blob object')
    
    index_entries = get_index_entries()

    # O is the stage number, where 
    # 0 - Normal (no conflict) — the version of the file ready to be committed, 
    # 1 - Base version (common ancestor in a merge)
    # 2 - "Ours" version (current branch during a merge)
    # 3 - "Theirs" version (branch being merged in)
    updated_entries = add_or_update_entry(index_entries, mode, 0, sha1_hex, filename)
    
    updated_index_content = b'\n'.join(updated_entries)

    compressed_index_content = zlib.compress(updated_index_content)
        
    with open(index_file_path, 'wb') as f:
        f.write(compressed_index_content)

