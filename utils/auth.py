from hashlib import sha1

def hash_password(password: str) -> str:
    return sha1(password.encode("utf8")).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed