import os
import zlib
import hashlib

from src.utils.constants import REPO_DIR_NAME, INDEX_FILE_NAME, OBJECTS_DIR_NAME

def write_tree() -> str:
    index_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, INDEX_FILE_NAME)
    with open(index_file_path, 'rb') as f:
        index_content = zlib.decompress(f.read())

    index_content_entries = index_content.split(b'\n')
    index_content_entries = [entry for entry in index_content_entries if entry]
    
    tree_entries = []
    tree_size = 0
    for entry in index_content_entries:
        mode, filename, _, sha1_hex = entry.split(b' ')
        tree_entry = mode + b" " + filename + b"\x00" + sha1_hex
        tree_entries.append(tree_entry)
        tree_size += len(tree_entry)

    tree_header = f"tree {tree_size}\0".encode()
    tree_content = b'\n'.join(tree_entries)
    tree_object = tree_header + tree_content

    tree_sha1 = hashlib.sha1(tree_object).hexdigest()

    # Write to .mygit/objects
    object_dir_path = os.path.join(os.getcwd(), REPO_DIR_NAME, OBJECTS_DIR_NAME, tree_sha1[:2])
    object_file_path = os.path.join(object_dir_path, tree_sha1[2:])

    # create the object directory if it doesn't exist
    os.makedirs(object_dir_path, exist_ok=True)

    # write the tree object to the file
    with open(object_file_path, 'wb') as f:
        f.write(zlib.compress(tree_object))

    return tree_sha1