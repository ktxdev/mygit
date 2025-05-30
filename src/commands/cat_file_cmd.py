from objects.object import get_object_content, get_object_type

def cat_file_cmd(object_hash: str, figure_out_type: bool) -> None:
    """
    Displays the contents of an object.
    """
    object_type = get_object_type(object_hash)
    if object_type == "blob":
        return get_object_content(object_hash)
    elif object_type == "tree":
        tree_content = get_object_content(object_hash)
        tree_entries = tree_content.split("\n")
        content = []
        for entry in tree_entries:
            mode, filename, sha1_hex = entry.split(" ")
            content.append(f"{mode} {get_object_type(sha1_hex)} {filename} {sha1_hex}")
        return "\n".join(content)
    else:
        raise ValueError(f"Unknown object type: {object_type}")
    


# TODO: add support for tree objects (Implement cat-file -p master^{tree})
