from datetime import datetime

from objects.object import get_object_type
from objects.object import get_object_content
from objects.commit import get_serialized_commit_history
from utils.diff import calculate_diff_from_tree

def log_cmd(commit_sha1: str) -> str:
    if get_object_type(commit_sha1) != "commit":
        raise ValueError("Provided SHA-1 is not for a commit object")
    
    log_entries = get_serialized_commit_history(commit_sha1)

    return "\n".join(log_entries)