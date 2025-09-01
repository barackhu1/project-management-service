from fastapi import APIRouter, Depends, HTTPException

from schemas import UserCreate
from crud import insert_user
from utils.auth import hash_password
from db import get_db

router = APIRouter(tags=["auth"])

@router.post("/auth")
def register_user(user: UserCreate, conn = Depends(get_db)):
    hashed = hash_password(user.password)
    try:
        db_user = insert_user(conn, user.username, hashed)
        return {
            "message": "User registered successfully",
            "user": db_user,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )