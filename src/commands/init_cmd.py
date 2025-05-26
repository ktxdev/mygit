import os

from src.utils.constants import *


class InitError(Exception):
    pass

def init_cmd() -> None:
    """
    Initializes a new mygit repository in the current working directory.

    Creates the basic directory structure with the following files:
    - .mygit directory
    - HEAD file
    - objects directory
    - refs directory
    - heads directory
    - config file

    Raises:
    - InitError: If the repository cannot be initialized.
    """
    try:
        repo_dir_path = os.path.join(os.getcwd(), REPO_DIR_NAME)
        os.makedirs(repo_dir_path, exist_ok=True)

        head_file_path = os.path.join(repo_dir_path, HEAD_FILE_NAME)
        config_file_path = os.path.join(repo_dir_path, CONFIG_FILE_NAME)

        with open(head_file_path, "w") as head_file:
            head_file.write(f"ref: {REFS_DIR_NAME}/{HEADS_DIR_NAME}/{DEFAULT_BRANCH_NAME}")


        open(config_file_path, "w").close()
        

        objects_dir_path = os.path.join(repo_dir_path, OBJECTS_DIR_NAME)
        refs_dir_path = os.path.join(repo_dir_path, REFS_DIR_NAME)

        os.makedirs(objects_dir_path, exist_ok=True)
        os.makedirs(refs_dir_path, exist_ok=True)

        print(f"Initialized empty mygit repository in {repo_dir_path}")
    except Exception as e:
        raise InitError(f"Failed to initialize repository: {e}")
    
    


