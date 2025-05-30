REPO_DIR_NAME = ".mygit"
INDEX_FILE_NAME = "index"
HEAD_FILE_NAME = "HEAD"
CONFIG_FILE_NAME = "config"
OBJECTS_DIR_NAME = "objects"
OBJECTS_DIR_SUBDIRS = ["pack", "info"]
HEADS_DIR_NAME = "heads"
REFS_DIR_NAME = "refs"
DEFAULT_BRANCH_NAME = "main"
VALID_BLOB_MODES = [
    100644, # normal file
    100755, # executable file
    120000, # Symbolic link
]