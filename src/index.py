import os
import zlib

from utils.constants import REPO_DIR_NAME, INDEX_FILE_NAME

def get_index_entries() -> list[bytes]:
    index_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, INDEX_FILE_NAME)
    with open(index_file_path, 'rb') as f:
        index_content = zlib.decompress(f.read())

    index_content_entries = index_content.split(b'\n')
    index_content_entries = [entry for entry in index_content_entries if entry]
    return index_content_entries

def save_index_entries(entries: list[bytes]) -> None:
    index_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, INDEX_FILE_NAME)

    with open(index_file_path, 'wb') as f:
        f.write(zlib.compress(b'\n'.join(entries)))

def clear_index() -> None:
    index_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, INDEX_FILE_NAME)
    with open(index_file_path, 'wb') as f:
        f.write(zlib.compress(b''))

def update_index_entry(mode: str, stage_number: int, sha1_hex: str, filename: str) -> None:
    """
    Updates the index entry for the given filename.

    Args:
        mode: The mode of the object.
        stage_number: The stage number of the object. 
            0 - Normal (no conflict)
            1 - base version (common ancestor in a merge), 
            2 - ours version (current branch during a merge),
            3 - theirs version (branch being merged in).
        sha1_hex: The SHA-1 hash of the object.
        filename: The filename of the object.

    Returns:
        None
    """
    entries = get_index_entries()

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

    save_index_entries(updated_entries)