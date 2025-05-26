import hashlib

def encode_content(content: bytes) -> str:
    return hashlib.sha1(content).hexdigest()