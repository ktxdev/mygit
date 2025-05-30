import hashlib

from index import clear_index, get_index_entries
from utils.constants import REPO_DIR_NAME, INDEX_FILE_NAME, OBJECTS_DIR_NAME
from objects.object import get_object_type, write_object

def write_tree() -> str:
    index_content_entries = get_index_entries()

    if not index_content_entries:
        raise ValueError("No index entries found")
    
    tree_entries = []
    tree_size = 0
    for entry in index_content_entries:
        mode, filename, _, sha1_hex = entry.split(b' ')
        object_type = get_object_type(sha1_hex.decode())

        tree_entry = mode + b" " + filename + b" " + sha1_hex
        tree_entries.append(tree_entry)
        tree_size += len(f"{mode} {filename}".encode()) + 21

    tree_content = b'\n'.join(tree_entries)
    tree_header = f"tree {tree_size}\0".encode()
    tree_content = tree_header + tree_content

    tree_sha1 = hashlib.sha1(tree_content).hexdigest()

    write_object(tree_content, tree_sha1)

    clear_index()

    return tree_sha1