from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from utils.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_access_token(token)
    return payload["user_id"]