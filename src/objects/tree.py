import os
import zlib

from src.utils.constants import REPO_DIR_NAME, INDEX_FILE_NAME

def write_tree() -> str:
    index_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, INDEX_FILE_NAME)
    with open(index_file_path, 'rb') as f:
        index_content = zlib.decompress(f.read())

    index_content_entries = index_content.split(b'\n')
    index_content_entries = [entry for entry in index_content_entries if entry]
    pass

def read_tree(sha1_hex: str) -> str:
    pass

def is_tree_object(sha1_hex: str) -> bool:
    pass