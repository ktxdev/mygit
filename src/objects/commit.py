import hashlib

from typing import Union
from datetime import datetime, timezone

from objects.object import write_object, get_object_content
from utils.config import get_config
from utils.diff import calculate_diff_from_tree

def write_commit(message: str, tree_sha1: str, parent_sha1: Union[str, None] = None) -> str:
    name = get_config("user.name")
    email = get_config("user.email")

    if not name or not email:
        raise ValueError("User name and email must be set")

    datetime_now = datetime.now(timezone.utc)
    timestamp = int(datetime_now.timestamp())
    timezone_offset = datetime_now.astimezone().strftime("%z")

    commit_content = f"tree {tree_sha1}"
    if parent_sha1:
        commit_content += f"\nparent {parent_sha1}"

    commit_content += f"\nauthor {name} <{email}> {timestamp} {timezone_offset}"
    commit_content += f"\ncommitter {name} <{email}> {timestamp} {timezone_offset}"
    commit_content += f"\n\n{message}"

    header = f"commit {len(commit_content)}\0".encode()
    commit_content = header + commit_content.encode()

    commit_sha1 = hashlib.sha1(commit_content).hexdigest()
    write_object(commit_content, commit_sha1)

    return commit_sha1

def serialize_commit(commit_sha1: str) -> list[str]:
    commit_content = get_object_content(commit_sha1)
    commit_entries = [entry for entry in commit_content.split("\n") if entry]

    serialized_entries = [f'commit {commit_sha1}']

    calculate_diff_from_tree(commit_entries[0].split(" ")[1])
    
    author_entry = commit_entries[2].split(" ")
    timezone_offset = author_entry[-1]
    timestamp = int(author_entry[-2])
    email = author_entry[-3]
    name = " ".join(author_entry[1:len(author_entry)-3])

    serialized_entries.append(f"Author: {name} {email}")
    serialized_entries.append(f"Date: {datetime.fromtimestamp(timestamp).strftime('%a %b %d %H:%M:%S %Y')} {timezone_offset}")
    serialized_entries.append(f"\n\t{commit_entries[-1]}\n")
    
    if len(commit_entries) == 5:
        parent_sha1 = commit_entries[1].split(" ")[1]
        serialized_entries.extend(serialize_commit(parent_sha1))
    
    return serialized_entries
