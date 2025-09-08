import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status

from app.config import SECRET_KEY

ENCRYPTION_ALGORITHMIC = "HS256"
CHARACTER_CODE = "utf-8"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(CHARACTER_CODE), bcrypt.gensalt()).decode(CHARACTER_CODE)

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(CHARACTER_CODE), hashed.encode(CHARACTER_CODE))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ENCRYPTION_ALGORITHMIC)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ENCRYPTION_ALGORITHMIC])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )