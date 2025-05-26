import os

from pathlib import Path

def status_cmd():
    repo_dir_path = os.getcwd()
    ignore_file_path = os.path.join(repo_dir_path, ".mygitignore")
    ignore_dirs = [str(os.path.join(repo_dir_path,".mygit"))]
    ignore_files = []

    if os.path.exists(ignore_file_path):
        files_and_dirs_to_ignore = []
        with open(ignore_file_path, "r") as ignore_file:
            files_and_dirs_to_ignore.extend(ignore_file.read().splitlines())
        
        for file_or_dir in files_and_dirs_to_ignore:
            if file_or_dir.startswith("**/"):
                file_or_dir = file_or_dir.replace("**/", "")
                ignore_dirs.append(file_or_dir.replace("/", ""))
            elif os.path.isdir(file_or_dir):
                ignore_dirs.append(file_or_dir.replace("/", ""))
            else:
                ignore_files.append(file_or_dir)

    def should_ignore_dir(dir_path: str) -> bool:
        abs_path = os.path.abspath(dir_path)
        return all(abs_path.startswith(ignore_dir) for ignore_dir in ignore_dirs)

    file_paths = []
    for root, dirs, files in os.walk(repo_dir_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        files[:] = [f for f in files if f not in ignore_files]
        
        for file in files:
            file_paths.append(os.path.join(root, file))
            
        
    print(file_paths)
    return file_paths


if __name__ == "__main__":
    status_cmd()
