import hashlib
from collections import deque
from typing import Union
from datetime import datetime, timezone

from objects.object import write_object, get_object_content
from utils.config import get_config
from utils.diff import calculate_diff_from_tree

def build_commit_history(commit_sha1: str) -> list[str]:
    history = deque()

    while commit_sha1:
        history.append(commit_sha1)
        commit_content = get_object_content(commit_sha1)
        commit_entries = [entry for entry in commit_content.split("\n") if entry]

        if len(commit_entries) == 5:
            commit_sha1 = commit_entries[1].split(" ")[1]
        else:
            commit_sha1 = None
    
    return history


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

def get_serialized_commit_history(commit_sha1: str, show_stats: bool = False) -> list[str]:
    """
    Builds and returns the full commit history (metadata + diffs) from oldest to newest.
    """
    history = build_commit_history(commit_sha1)
    return serialize_commit_history(history, show_stats)


def format_commit_metadata(commit_sha1: str) -> list[str]:
    """
    Returns a formatted commit header: SHA, Author, Date, and message.
    """
    commit_content = get_object_content(commit_sha1)
    commit_entries = [entry for entry in commit_content.split("\n") if entry]

    serialized = [f'commit {commit_sha1}']
    
    author_entry = commit_entries[2].split(" ")
    timezone_offset = author_entry[-1]
    timestamp = int(author_entry[-2])
    email = author_entry[-3]
    name = " ".join(author_entry[1:-3])

    serialized.append(f"Author: {name} {email}")
    serialized.append(f"Date: {datetime.fromtimestamp(timestamp).strftime('%a %b %d %H:%M:%S %Y')} {timezone_offset}")
    serialized.append(f"\n\t{commit_entries[-1]}\n")

    return serialized


def generate_commit_diff(current_commit_sha1: str, previous_commit_sha1: str = None) -> list[str]:
    """
    Returns formatted diff between two commits or from empty state if no parent.
    """
    current_content = get_object_content(current_commit_sha1)
    current_entries = [entry for entry in current_content.split("\n") if entry]
    current_tree_sha1 = current_entries[0].split(" ")[1]

    if not previous_commit_sha1:
        diff = calculate_diff_from_tree(tree_sha1=current_tree_sha1)
        return [f"\n{diff}\n"]

    previous_content = get_object_content(previous_commit_sha1)
    previous_entries = [entry for entry in previous_content.split("\n") if entry]
    previous_tree_sha1 = previous_entries[0].split(" ")[1]

    diff = calculate_diff_from_tree(tree_sha1=current_tree_sha1, parent_tree_sha1=previous_tree_sha1)
    return [f"\n{diff}\n"]


def serialize_commit_history(history: deque, show_stats: bool = False) -> list[str]:
    """
    Recursively serializes a list of commits and diffs from oldest to newest.
    """
    if len(history) == 1:
        current_sha1 = history.popleft()
        output = format_commit_metadata(current_sha1)
        if show_stats:
            output.extend(generate_commit_diff(current_sha1))
        return output

    current_sha1 = history.popleft()
    output = format_commit_metadata(current_sha1)
    if show_stats:
        output.extend(generate_commit_diff(current_sha1, history[0]))

    return output + serialize_commit_history(history, show_stats)
