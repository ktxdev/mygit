import os

REPO_DIR_NAME = ".mygit"
HEAD_FILE_NAME = "HEAD"
CONFIG_FILE_NAME = "config"
OBJECTS_DIR_NAME = "objects"
REFS_DIR_NAME = "refs"



def init_cmd():
    repo_dir_path = os.path.join(os.getcwd(), REPO_DIR_NAME)
    os.makedirs(repo_dir_path, exist_ok=True)

    head_file_path = os.path.join(repo_dir_path, HEAD_FILE_NAME)
    config_file_path = os.path.join(repo_dir_path, CONFIG_FILE_NAME)

    open(head_file_path, "w").close()
    open(config_file_path, "w").close()

    objects_dir_path = os.path.join(repo_dir_path, OBJECTS_DIR_NAME)
    refs_dir_path = os.path.join(repo_dir_path, REFS_DIR_NAME)

    os.makedirs(objects_dir_path, exist_ok=True)
    os.makedirs(refs_dir_path, exist_ok=True)

    print(f"Initialized empty mygit repository in {repo_dir_path}")
    
    


