from src.objects.blob import read_blob

def cat_file_cmd(object_hash: str, figure_out_type: bool) -> None:
    """
    Displays the contents of an object.
    """
    object_type, content = get_object_type_and_content(object_hash)

    if object_type == "blob":
        return content
    else:
        raise ValueError(f"Unknown object type: {object_type}")
    
def get_object_type_and_content(object_hash: str) -> tuple[str, str]:
    """
    Gets the type of an object.
    """
    content = read_blob(object_hash)

    header, content = content.decode().split("\0", 1)
    object_type, _ = header.split(" ")

    return object_type, content

# TODO: add support for tree objects (Implement cat-file -p master^{tree})
