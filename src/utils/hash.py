import hashlib

def hash_file(file_path: str, chunk_size: int = 8192) -> str:
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha1.update(chunk)
    return sha1.hexdigest()