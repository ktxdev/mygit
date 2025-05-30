import os
import zlib

from src.utils.constants import *


class InitError(Exception):
    pass

def init_cmd(dir_path: str = '.') -> None:
    """
    Initializes a new mygit repository in the current working directory or in the given directory.

    Creates the basic directory structure with the following files:
    - .mygit directory
    - objects directory

    Raises:
    - InitError: If the repository cannot be initialized.
    """
    try:
        repo_dir_path = os.path.join(os.path.abspath(dir_path), REPO_DIR_NAME)
        os.makedirs(repo_dir_path, exist_ok=True)

        os.makedirs(os.path.join(repo_dir_path, OBJECTS_DIR_NAME), exist_ok=True)
        for subdir in OBJECTS_DIR_SUBDIRS:
            os.makedirs(os.path.join(repo_dir_path, OBJECTS_DIR_NAME, subdir), exist_ok=True)

        with open(os.path.join(repo_dir_path, INDEX_FILE_NAME), 'wb') as f:
            f.write(zlib.compress(b''))
        

        print(f"\nInitialized empty mygit repository in {repo_dir_path}")
    except Exception as e:
        raise InitError(f"Failed to initialize repository: {e}")
    
    


