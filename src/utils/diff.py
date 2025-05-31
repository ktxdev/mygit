from objects.object import get_object_content


def calculate_diff(old_content: str, new_content: str = None) -> tuple[int, int]:
    old_lines = old_content.split("\n") if old_content else []
    new_lines = new_content.split("\n") if new_content else []

    insertions = 0
    deletions = 0

    min_length = min(len(old_lines), len(new_lines))

    for i in range(min_length):
        if old_lines[i] != new_lines[i]:
            deletions += 1
            insertions += 1

    if len(new_lines) > min_length:
        insertions += len(new_lines) - min_length
    elif len(old_lines) > min_length:
        deletions += len(old_lines) - min_length

    return insertions, deletions

def calculate_diff_from_tree(tree_sha1: str, parent_tree_sha1: str = None) -> str:
    tree_content = get_object_content(tree_sha1)
    tree_entries = tree_content.split("\n")
    tree_entries = [entry for entry in tree_entries if entry]

    if parent_tree_sha1:
        parent_tree_content = get_object_content(parent_tree_sha1)
        parent_tree_entries = parent_tree_content.split("\n")
        parent_tree_entries = [entry for entry in parent_tree_entries if entry]

        for parent_tree_entry in parent_tree_entries:
            _, filename, object_sha1 = parent_tree_entry.split(" ")
            insertions, deletions = calculate_diff(get_object_content(object_sha1))
            print(f"{filename} | {'+' * insertions} {'-' * deletions}")

    for tree_entry in tree_entries:
        _, filename, object_sha1 = tree_entry.split(" ")
        insertions, deletions = calculate_diff(get_object_content(object_sha1))
        print(f"{filename} | {'+' * insertions} {'-' * deletions}")
    