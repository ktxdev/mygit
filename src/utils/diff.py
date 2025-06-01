from objects.object import get_object_content


def calculate_diff(old_content: str = None, new_content: str = None) -> tuple[int, int]:
    old_lines = old_content.strip().split("\n") if old_content else []
    new_lines = new_content.strip().split("\n") if new_content else []

    insertions = deletions = 0

    old_set = set(old_lines)
    new_set = set(new_lines)

    insertions = len(new_set - old_set)
    deletions = len(old_set - new_set)

    return insertions, deletions
    

def calculate_diff_from_tree(tree_sha1: str, parent_tree_sha1: str = None, path_prefix: str = "") -> str:
    def parse_tree(tree_content):
        entries = []
        for line in tree_content.strip().split("\n"):
            parts = line.strip().split(" ")
            if len(parts) == 3:
                mode, filename, sha1 = parts
                type_ = "tree" if mode == "040000" else "blob"
            elif len(parts) == 4:
                mode, type_, filename, sha1 = parts
            else:
                continue
            entries.append((mode, type_, filename, sha1))
        return entries

    current_tree = {e[2]: e for e in parse_tree(get_object_content(tree_sha1))}
    parent_tree = {}
    if parent_tree_sha1:
        parent_tree = {e[2]: e for e in parse_tree(get_object_content(parent_tree_sha1))}

    stats = []
    total_insertions = 0
    total_deletions = 0
    changed_files = 0

    # Files in both trees or removed
    for filename, (p_mode, p_type, _, p_sha1) in parent_tree.items():
        p_path = path_prefix + filename
        if p_type == "tree":
            if filename in current_tree and current_tree[filename][1] == "tree":
                child = calculate_diff_from_tree(
                    tree_sha1=current_tree[filename][3],
                    parent_tree_sha1=p_sha1,
                    path_prefix=p_path + "/"
                )
                if child:
                    stats.append(child)
            continue

        if filename in current_tree:
            _, c_type, _, c_sha1 = current_tree[filename]
            if c_type == "blob":
                insertions, deletions = calculate_diff(
                    old_content=get_object_content(p_sha1),
                    new_content=get_object_content(c_sha1)
                )
        else:
            insertions, deletions = calculate_diff(old_content=get_object_content(p_sha1), new_content="")

        if insertions > 0 or deletions > 0:
            changed_files += 1
            total_insertions += insertions
            total_deletions += deletions
            stats.append(f"{p_path} | {insertions + deletions} {'+' * insertions}{'-' * deletions}")

    # New files
    for filename, (c_mode, c_type, _, c_sha1) in current_tree.items():
        if filename not in parent_tree:
            c_path = path_prefix + filename
            if c_type == "tree":
                child = calculate_diff_from_tree(
                    tree_sha1=c_sha1,
                    parent_tree_sha1=None,
                    path_prefix=c_path + "/"
                )
                if child:
                    stats.append(child)
                continue

            insertions, deletions = calculate_diff(new_content=get_object_content(c_sha1), old_content="")
            if insertions > 0 or deletions > 0:
                changed_files += 1
                total_insertions += insertions
                total_deletions += deletions
                stats.append(f"{c_path} | {insertions + deletions} {'+' * insertions}{'-' * deletions}")

    if changed_files > 0:
        summary = f"{changed_files} file{'s' if changed_files != 1 else ''} changed"
        if total_insertions > 0:
            summary += f", {total_insertions} insertion{'s' if total_insertions != 1 else ''}(+)"
        if total_deletions > 0:
            summary += f", {total_deletions} deletion{'s' if total_deletions != 1 else ''}(-)"
        stats.append(summary)

    return "\n".join(stats)
