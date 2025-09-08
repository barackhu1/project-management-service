from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.schemas import UserCreate, UserLogin
from app.crud.users import insert_user, get_user_by_username
from app.utils.auth import hash_password, verify_password, create_access_token
from app.utils.db import get_db

router = APIRouter(tags=["auth"])

@router.post("/auth")
def register_user(user: UserCreate, conn = Depends(get_db)):
    hashed = hash_password(user.password)
    try:
        db_user = insert_user(conn, user.username, hashed)
        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "User registered successfully",
            "user": db_user,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

@router.post("/login")
def login_user(form: OAuth2PasswordRequestForm = Depends(), conn = Depends(get_db)):
    username = form.username
    password = form.password

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or password is required")

    user = get_user_by_username(conn, username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_id = user[0]
    stored_password_hash = user[2]

    if not verify_password(password, stored_password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token_data = {"user_id": user_id, "username": username}
    access_token = create_access_token(token_data)

    return {
        "status_code": status.HTTP_200_OK,
        "message": "Login successful",
        "user_id": user_id,
        "username": username,
        "access_token": access_token,
        "token_type": "bearer",
    }